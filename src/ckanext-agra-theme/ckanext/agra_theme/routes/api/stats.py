import requests
from ckan.model import Session, Vocabulary, Tag, PackageTag
from sqlalchemy import func
from flask import jsonify, request


def api_stats(blueprint):
    @blueprint.route("/api/2/statistic/<vocab>", methods=["GET"])
    def statistic(vocab):
        vocab = vocab.lower()
        vocab_obj = Vocabulary.get(vocab)
        if not vocab_obj:
            return jsonify({"error": "Vocabulary not found"}), 404

        # All Counts
        # counts = (
        #     Session.query(
        #         Tag.name, func.count(PackageTag.tag_id)
        #     )  # Use the imported func
        #     .join(PackageTag, Tag.id == PackageTag.tag_id)
        #     .filter(Tag.vocabulary_id == vocab_obj.id)
        #     .group_by(Tag.name)
        #     .all()
        # )

        # Top 5
        counts = (
            Session.query(Tag.name, func.count(PackageTag.tag_id))
            .join(PackageTag, Tag.id == PackageTag.tag_id)
            .filter(Tag.vocabulary_id == vocab_obj.id)
            .group_by(Tag.name)
            .order_by(
                func.count(PackageTag.tag_id).desc()
            )  # Order by count DESCENDING
            .limit(5)  # Limit to the top 5
            .all()
        )

        # Format the results into a list of dictionaries
        results = [{"name": name, "value": count} for name, count in counts]

        return jsonify(results)
