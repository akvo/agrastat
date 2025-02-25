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
        # Define the context (required for CKAN actions)
        context = {
            "ignore_auth": True
        }  # Use appropriate auth settings as needed

        try:
            # Fetch all users in the organization
            users = toolkit.get_action("member_list")(
                context=context, data_dict={"id": org_id, "object_type": "user"}
            )

            # Prepare a list to store user names and their dataset counts
            user_counts = []

            # Iterate over each user in the organization
            for user_id, _, _ in users:
                # Fetch user details
                user = toolkit.get_action("user_show")(
                    context=context, data_dict={"id": user_id}
                )

                # Count datasets created by the user in the organization (including private datasets)
                dataset_count = toolkit.get_action("package_search")(
                    context=context,
                    data_dict={
                        "fq": f"organization:{org_id} AND creator_user_id:{user_id} AND (private:true OR private:false)",
                        "rows": 0,  # We only need the count, not the actual datasets
                    },
                )["count"]

                # Append the user's name and dataset count to the list
                user_counts.append(
                    (user.get("fullname") or user["name"], dataset_count)
                )

            # Sort users by dataset count in descending order and return the top 3
            return sorted(user_counts, key=lambda x: x[1], reverse=True)[:3]

        except toolkit.ObjectNotFound:
            # Handle case where the organization ID is invalid
            return []
        except Exception as e:
            # Log any unexpected errors
            toolkit.error_shout(f"An error occurred: {str(e)}")
            return []

    def _get_top_datasets_by_followers(org_id):
        # Define the context (required for CKAN actions)
        context = {
            "ignore_auth": True
        }  # Use appropriate auth settings as needed

        # Fetch all datasets in the organization
        datasets = toolkit.get_action("package_search")(
            context=context,
            data_dict={
                "fq": f"organization:{org_id}",
                "rows": 1000,  # Adjust this value based on your needs
            },
        )["results"]

        # Fetch follower counts for each dataset using dataset_follower_count
        dataset_followers = []
        for ds in datasets:
            follower_count = toolkit.get_action("dataset_follower_count")(
                context=context, data_dict={"id": ds["id"]}
            )
            dataset_followers.append((ds["title"], follower_count))

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
            dataset_views.append((ds["title"], views))
        print(dataset_views)
        return sorted(dataset_views, key=lambda x: x[1], reverse=True)[:5]

    def _get_top_datasets_by_views(org_id):
        datasets = toolkit.get_action("package_search")(
            data_dict={"fq": f"organization:{org_id}", "rows": 1000}
        )["results"]
        dataset_views = []
        for ds in datasets:
            stats = toolkit.get_action("package_show")({}, {"id": ds["id"]})
            views = stats.get("tracking_summary", {}).get("total", 0)
            dataset_views.append((ds["title"], views))
        print(dataset_views)
        return sorted(dataset_views, key=lambda x: x[1], reverse=True)[:5]
