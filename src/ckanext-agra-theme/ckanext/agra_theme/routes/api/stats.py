from ckan.model import Session, Package, Tag, Vocabulary, PackageTag
from sqlalchemy import func
from flask import request, jsonify
from ckan.plugins import toolkit
from ckan.plugins.toolkit import get_action


def api_stats(blueprint):
    @blueprint.route("/api/2/statistic/<vocab>", methods=["GET"])
    def statistic(vocab):
        vocab = vocab.lower()
        limit = request.args.get("limit", None)
        organization = request.args.get("organization", None)

        # Fetch the vocabulary object
        vocab_obj = Vocabulary.get(vocab)
        if not vocab_obj:
            return jsonify({"error": "Vocabulary not found"}), 404

        # Base query for counting tags
        query = (
            Session.query(Tag.name, func.count(PackageTag.tag_id))
            .join(
                PackageTag, Tag.id == PackageTag.tag_id
            )  # Join Tag to PackageTag
            .filter(Tag.vocabulary_id == vocab_obj.id)
        )

        # Validate and filter by organization
        if organization:
            context = {"user": toolkit.g.user}
            try:
                org = get_action("organization_show")(
                    context, {"id": organization}
                )
                org_id = org["id"]  # Get the correct organization ID
                print(f"Valid Organization: {org['name']} ({org_id})")
            except toolkit.ObjectNotFound:
                return jsonify({"error": "Organization not found"}), 404
            except Exception as e:
                return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

            query = query.join(
                Package, PackageTag.package_id == Package.id
            ).filter(  # Join PackageTag to Package
                Package.owner_org == org_id
            )  # Use correct org ID

        # Apply ordering and limiting
        query = query.group_by(Tag.name).order_by(
            func.count(PackageTag.tag_id).desc()
        )

        if limit:
            try:
                limit = int(limit)
                query = query.limit(limit)
            except ValueError:
                return jsonify({"error": "Invalid limit value"}), 400

        # Execute the query
        counts = query.all()

        # Handle empty results
        if not counts:
            return (
                jsonify(
                    {"message": "No data found for the specified organization"}
                ),
                200,
            )

        # Format the results into a list of dictionaries
        results = [{"name": name, "value": count} for name, count in counts]
        return jsonify(results)
