import ckan.plugins.toolkit as toolkit
from flask import Blueprint, request, make_response
import pandas as pd


def page_external(blueprint):
    @blueprint.route("/faostat")
    def faostat_page():
        page = request.args.get("page", "")
        return toolkit.render("faostat.html", {"page": page})

    @blueprint.route("/convert", methods=["GET", "POST"])
    def convert():
        if request.method == "GET":
            # Render the upload form for GET requests
            return toolkit.render("converter.html")

        if request.method == "POST":
            try:
                # Get the uploaded file from the request
                uploaded_file = request.files.get("file")
                if not uploaded_file:
                    return toolkit.abort(400, "No file uploaded.")

                # Save the uploaded file temporarily
                file_path = f"/tmp/{uploaded_file.filename}"
                uploaded_file.save(file_path)

                # Convert the file to a pandas DataFrame based on its format
                df = None
                if uploaded_file.filename.endswith((".xlsx", ".xls")):
                    df = pd.read_excel(file_path)
                elif uploaded_file.filename.endswith(".dta"):
                    df = pd.read_stata(file_path)
                else:
                    return toolkit.abort(
                        400,
                        "Unsupported file format. Only .xlsx, .xls, and .dta files are allowed.",
                    )

                # Generate the output CSV file path
                csv_filename = f"{uploaded_file.filename.split('.')[0]}.csv"
                csv_path = f"/tmp/{csv_filename}"

                # Save the DataFrame as a CSV file
                df.to_csv(csv_path, index=False)

                # Return the CSV file as a downloadable response
                with open(csv_path, "rb") as csv_file:
                    response = make_response(csv_file.read())
                    response.headers["Content-Type"] = "text/csv"
                    response.headers[
                        "Content-Disposition"
                    ] = f"attachment; filename={csv_filename}"
                    return response

            except Exception as e:
                return toolkit.abort(500, f"An error occurred: {str(e)}")
