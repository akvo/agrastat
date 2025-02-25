import ckan.plugins.toolkit as toolkit


def page_statistic(blueprint):
    @blueprint.route("/organization/stats/<id>")
    def stats(id):
        # Set up the context for accessing CKAN actions
        context = {"user": toolkit.g.user}
        try:
            # Ensure the organization exists
            org = toolkit.get_action("organization_show")(context, {"id": id})
        except toolkit.ObjectNotFound:
            return toolkit.abort(404, description="Organization not found")

        # Get top 5 users by dataset count
        top_users = _get_top_users_by_dataset_count(id)

        # Get top 5 datasets by follower count
        top_datasets_by_followers = _get_top_datasets_by_followers(id)

        # Get top 5 datasets by view count (requires stats plugin)
        top_datasets_by_views = _get_top_datasets_by_views(id)

        # Render the template with the statistics data
        return toolkit.render(
            "organization/stats.html",
            {
                "org": org,
                "group_dict": org,  # Pass the organization as group_dict
                "group_type": "organization",  # Define group_type explicitly
                "g": toolkit.g,  # Pass CKAN's global object
                "h": toolkit.h,  # Pass CKAN's helper functions
                "top_users": top_users,
                "top_datasets_by_followers": top_datasets_by_followers,
                "top_datasets_by_views": top_datasets_by_views,
            },
        )

    def _get_top_users_by_dataset_count(org_id):
        users = toolkit.get_action("member_list")(
            data_dict={"id": org_id, "object_type": "user"}
        )
        user_counts = []
        for user_id, _, _ in users:
            user = toolkit.get_action("user_show")(data_dict={"id": user_id})
            dataset_count = len(
                toolkit.get_action("package_search")(
                    data_dict={
                        "fq": f"organization:{org_id} AND creator_user_id:{user_id}"
                    }
                )["results"]
            )
            user_counts.append((user["name"], dataset_count))
        return sorted(user_counts, key=lambda x: x[1], reverse=True)[:5]

    def _get_top_datasets_by_followers(org_id):
        # Fetch all datasets in the organization
        datasets = toolkit.get_action("package_search")(
            data_dict={
                "fq": f"organization:{org_id}",
                "rows": 1000,
            }
        )["results"]

        # Fetch follower counts for each dataset using package_show
        dataset_followers = []
        for ds in datasets:
            dataset = toolkit.get_action("package_show")(
                data_dict={"id": ds["id"], "include": "num_followers"}
            )
            num_followers = dataset.get("num_followers", 0)
            dataset_followers.append((ds["name"], num_followers))

        # Sort datasets by follower count and return the top 5
        return sorted(dataset_followers, key=lambda x: x[1], reverse=True)[:5]

    def _get_top_datasets_by_views(org_id):
        datasets = toolkit.get_action("package_search")(
            data_dict={"fq": f"organization:{org_id}", "rows": 1000}
        )["results"]
        dataset_views = []
        for ds in datasets:
            stats = toolkit.get_action("package_show")({}, {"id": ds["id"]})
            views = stats.get("tracking_summary", {}).get("total", 0)
            dataset_views.append((ds["name"], views))
        return sorted(dataset_views, key=lambda x: x[1], reverse=True)[:5]
