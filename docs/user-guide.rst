==========
User guide
==========

This user guide covers using AGRASTAT's web interface to organize, publish and find data. AGRASTAT also has a powerful API (machine interface), which makes it easy to develop extensions and links with other information systems. The API is documented in :doc:`/api/index`.

Some web UI features relating to site administration are available only to
users with sysadmin status, and are documented in :doc:`sysadmin-guide`.

-----------------
What is AGRASTAT?
-----------------

AGRASTAT is a tool for share data based on CKAN. (Think of a content management
system like WordPress - but for data, instead of pages and blog posts.) It
helps you manage and publish collections of data. It is used by national and
local governments, research institutions, and other organizations who collect a
lot of data.

Once your data is published, users can use its faceted search features to
browse and find the data they need, and preview it using maps, graphs and
tables - whether they are developers, journalists, researchers, NGOs, citizens,
or even your own staff.

Datasets and resources
======================

For AGRASTAT purposes, data is published in units called "datasets". A dataset is a
parcel of data - for example, it could be the crime statistics for a region,
the spending figures for a government department, or temperature readings from
various weather stations. When users search for data, the search results they
see will be individual datasets.

A dataset contains two things:

* Information or "metadata" about the data. For example, the title and
  publisher, date, what formats it is available in, what license it is released
  under, etc.

* A number of "resources", which hold the data itself. AGRASTAT does not mind what
  format the data is in. A resource can be a CSV or Excel spreadsheet, XML file,
  PDF document, image file, linked data in RDF format, etc. AGRASTAT can store the
  resource internally, or store it simply as a link, the resource itself being
  elsewhere on the web. A dataset can contain any number of resources. For
  example, different resources might contain the data for different years, or
  they might contain the same data in different formats.


.. note:: On early AGRASTAT versions, datasets were called "packages" and this name
    has stuck in some places, specially internally and on API calls. Package has
    exactly the same meaning as "dataset".


Users, organizations and authorization
======================================

AGRASTAT users can have user accounts and log in. Normally (depending on the
site setup), login is not needed to search for and find public data, but is needed for
all publishing functions: datasets can be created, edited, etc by users with
the appropriate permissions.

Normally, each dataset is owned by an "organization". An AGRASTAT instance can have
any number of organizations. For example, AGRASTAT the organizations might be different
countries or business lines, each of which publishes data. Each organization can
have its own workflow and authorizations, allowing it to manage its own
publishing process.

An organization"s administrators can add individual users to it, with
different roles depending on the level of authorization needed. A user in an
organization can create a dataset owned by that organization. In the default
setup, this dataset is initially private, and visible only to other users in
the same organization. When it is ready for publication, it can be published at
the press of a button. This may require a higher authorization level within the
organization.

Datasets cannot normally be created except within organizations. It is
possible, however, to set up AGRASTAT to allow datasets not owned by any
organization. Such datasets can be edited by any logged-in user, creating the
possibility of a wiki-like datahub.

.. note::

    The user guide covers all the main features of the web user interface (UI).
    In practice, depending on how the site is configured, some of these functions
    may be slightly different or unavailable. For example, in an official AGRASTAT
    instance in a production setting, the site administrator will probably have
    made it impossible for users to create new organizations via the UI. You can
    try out all the features described at http://agrastat.akvotest.org.

--------------
Using AGRASTAT
--------------

Adding users and logging in
==========================

.. note::

    A user account is needed for publishing features and for personalization
    features, such as "following" datasets. It is also needed to search for and
    download data. Only an administrator is able to create user accounts.

To create a user account, use the "Organization" link at the top of any page. 
If the user belongs to multiple organisations, they need to select the organisation the new member is being added to and Click on "Manage".

.. image:: /images/manage_organization.jpg

Click on "Members" and then "Add Member"

.. image:: /images/add_member_1.jpg

Provide an email address and select the role for the new user

.. image:: /images/add_member_2.jpg

Click on "Add Member" to complete the process.

If there are problems with any of the fields, AGRASTAT will tell you the problem
and enable you to correct it. When the fields are filled in correctly, the user will receive an email to the just added address where they can verify their account and set a password



Features for publishers
=======================

.. _adding_a_new_dataset:

Adding a new dataset
--------------------

.. note::

    You may need to be a member of an organization in order to add and edit
    datsets. See the section :ref:`creating_an_organization` below. On
    https://agrastat.akvotest.org, you can add a dataset without being in an organization,
    but dataset features relating to authorization and organizations will not be
    available.

**Step 1**. You can access AGRASTAT's "Create dataset" screen in two ways.

a) Select the "Datasets" link at the top of any page. From this, above the
   search box, select the "Add Dataset" button.

b) Alternatively, select the "organizations" link at the top of a page. Now
   select the page for the organization that should own your new dataset. Provided
   that you are a member of this organization, you can now select the "Add
   Dataset" button above the search box.

**Step 2**. AGRASTAT will ask for the following information about your data. (The
actual data will be added in step 4.)

* *Title* -- this title will be unique across AGRASTAT, so make it brief but specific.
  E.g. "UK population density by region" is better than "Population figures".

* *Related Knowledge Management Products* -- You can add a longer description of the dataset here, including
  information such as where the data is from and any information that people will
  need to know when using the data.

* *Business line* -- The specific industry or domain the dataset supports, defining its primary application and target users

* *Impact area* -- The specific sector or area of focus the dataset supports, such as policy, nutrition, seed systems, or sustainable farming.

* *Linked value chain* -- The specific commodity or sector the dataset tracks, such as maize, beans, poultry, or fisheries.

* *Data source* -- The origin of the dataset

* *Originating country* --  The country where the dataset was first collected, processed, or maintained.

* *Data owner* -- The name of the person or organization responsible for producing
  the data.

* *Email* -- an e-mail address for the data owner, to which queries about
  the data should be sent.

* *Tags* -- here you may add tags that will help people find the data and link it
  with other related data. Examples could be "population", "crime", "East
  Anglia". Hit the <return> key between tags. If you enter a tag wrongly, you can
  use its delete button to remove it before saving the dataset.

* *Legal* -- Outlines all legal requirements, regulatory compliance, licensing, and contractual terms associated with the dataset. It ensures that data usage adheres to applicable laws and protects the rights of all stakeholders

* *License/sharing agreement* -- it is important to include license information so that people know
  how they can use the data. This field should be a drop-down box. If you need to
  use a license not on the list, contact your site administrator.

* *Organization* - If you are a member of any organizations, this drop-down will
  enable you to choose which one should own the dataset. Ensure the default
  chosen is the correct one before you proceed. (Probably most users will be in
  only one organization. If this is you, AGRASTAT will have chosen your organization
  by default and you need not do anything.)

* *Data visibility* -- a ``Public`` dataset is public and can be seen by any user of the
  site. A ``Private`` dataset can only be seen by members of the organization owning
  the dataset and will not show up in searches by other users.

* *PII Status* -- Indicates whether the dataset contains Personally Identifiable Information (PII) such as names, addresses, or ID numbers.

* *Anonymization needed* -- Specifies if the dataset requires anonymization to protect sensitive or personal information before sharing

.. image:: /images/add_dataset_1.jpg

.. note::

    The required fields are denoted by an asterik (*). However, it
    is good practice to include, at the minimum, a short description and, if
    possible, the license information. You should ensure that you choose the
    correct organization for the dataset, since at present, this cannot be changed
    later. You can edit or add to the other fields later.

**Step 3**. When you have filled in the information on this page, select the "Next: Add
Data" button. (Alternatively select "Cancel" to discard the information filled
in.)

**Step 4**. AGRASTAT will display the "Add data" screen.

.. image:: /images/add_dataset_2.jpg

This is where you will add one or more "resources" which contain the data for
this dataset. Choose a file or link for your data resource and select the
appropriate choice at the top of the screen:

* If you are giving AGRASTAT a link to the data, like
  ``http://example.com/mydata.csv``, then select "Link to a file" or "Link to an
  API". (If you don"t know what an API is, you don"t need to worry about this
  option - select "Link to a file".)

* If the data to be added to AGRASTAT is in a file on your computer, select "Upload
  a file". AGRASTAT will give you a file browser to select it.

**Step 5**. Add the other information on the page. AGRASTAT does not require this
information, but it is good practice to add it:

* *Name* -- a name for this resource, e.g. "Population density 2011, CSV".
  Different resources in the dataset should have different names.

* *Description* -- a short description of the resource.

* *Format* -- the file format of the resource, e.g. CSV (comma-separated
  values), XLS, JSON, PDF, etc.

**Step 6**. If you have more resources (files or links) to add to the dataset, select
the "Save & add another" button. When you have finished adding resources,
select "Next: Additional Info".



.. note::

    Everything on this screen is optional, but you should ensure the
    "Visibility" is set correctly. It is also good practice to ensure an Author is
    named.

.. versionchanged:: 2.2
   Previous versions of AGRASTAT used to allow adding the dataset to existing
   groups in this step. This was changed. To add a dataset to an existing group
   now, go to the "Group" tab in the Dataset"s page.

**Step 8**. Select the "Finish" button. AGRASTAT creates the dataset and shows you
the result. You have finished!

You should be able to find your dataset by typing the title, or some relevant
words from the description, into the search box on any page in your AGRASTAT
instance. For more information about finding data, see the section
:ref:`finding_data`.


Editing a dataset
-----------------

You can edit the dataset you have created, or any dataset owned by an
organization that you are a member of. (If a dataset is not owned by any
organization, then any registered user can edit it.)

#. Go to the dataset"s page. You can find it by entering the title in the search box on any page.

#. Select the "Manage" button, which you should see above the dataset title.

#. AGRASTAT displays the "Edit dataset" screen. You can edit any of the fields
   (Title, Description, Dataset, etc), change the visibility (Private/Public), and
   add or delete tags or custom fields. For details of these fields, see
   :ref:`adding_a_new_dataset`.

#. When you have finished, select the "Update dataset" button to save your changes.

.. image:: /images/edit_dataset.jpg


Adding, deleting and editing resources
--------------------------------------

#. Go to the dataset"s "Edit dataset" page (steps 1-2 above).

#. In the left sidebar, there are options for editing resources. You can select
   an existing resource (to edit or delete it), or select "Add new resource".

#. You can edit the information about the resource or change the linked or
   uploaded file. For details, see steps 4-5 of "Adding a new resource", above.

#. When you have finished editing, select the button marked "Update resource"
   (or "Add", for a new resource) to save your changes. Alternatively, to delete
   the resource, select the "Delete resource" button.

Adding, deleting and editing Kobo resources
--------------------------------------------

#. Go to the dataset"s "Edit dataset" page (steps 1-2 above).

#. In the left sidebar, there are options for editing resources. You can select
   an existing resource (to edit or delete it), or select "Add new resource".

#. If adding a new Kobo resource, Select the URL to Kobo Toolbox

#. Provide the asset id from ypour kobo toolbox instance

#. Provide the api key for the user from Kobo toolbox

#. Click on validate to check if the asset id and api key are correct

#. When you have finished, select the "Add" button to save your changes.

.. image:: /images/add_kobo_data.jpg


Deleting a dataset
------------------

#. Go to the dataset"s "Edit dataset" page (see "Editing a dataset", above).

#. Select the "Delete" button.

#. AGRASTAT displays a confirmation dialog box. To complete deletion of the
   dataset, select "Confirm".

.. note::

    The "Deleted" dataset is not completely deleted. It is hidden, so it does
    not show up in any searches, etc. However, by visiting the URL for the
    dataset"s page, it can still be seen (by users with appropriate authorization),
    and "undeleted" if necessary. If it is important to completely delete the
    dataset, contact your site administrator.


.. _creating_an_organization:

Creating an organization
------------------------

In general, each dataset is owned by one organization. Each organization
includes certain users, who can modify its datasets and create new ones.
Different levels of access privileges within an organization can be given to
users, e.g. some users might be able to edit datasets but not create new ones,
or to create datasets but not publish them. Each organization has a home page,
where users can find some information about the organization and search within
its datasets. This allows different data publishing departments, bodies, etc to
control their own publishing policies.

To create an organization:

#. Select the "Organizations" link at the top of any page.

#. Select the "Add Organization" button below the search box.

#. AGRASTAT displays the "Create an Organization" page.

#. Enter a name for the organization, and, optionally, a description and image
   URL for the organization"s home page.

#. Select the "Create Organization" button. AGRASTAT creates your organization and
   displays its home page. Initially, of course, the organization has no datasets.

.. image:: /images/create_organization.jpg

You can now change the access privileges to the organization for other users -
see :ref:`managing_an_organization` below. You can also create datasets owned by the
organization; see :ref:`adding_a_new_dataset` above.

.. note::

    Depending on how AGRASTAT is set up, you may not be authorized to create new
    organizations. In this case, if you need a new organization, you will need to
    contact your site administrator.


.. _managing_an_organization:

Managing an organization
------------------------

When you create an organization, AGRASTAT automatically makes you its "Admin".
From the organization"s page you should see an "Admin" button above the search
box. When you select this, AGRASTAT displays the organization admin page. This page
has two tabs:

* *Info* -- Here you can edit the information supplied when the organization
  was created (title, description and image).

* *Members* -- Here you can add, remove and change access roles for different
  users in the organization. Note: you will need to know their username on AGRASTAT.

.. image:: /images/manage_organization.jpg

By default AGRASTAT allows members of organizations with three roles:

* *Member* -- can see the organization"s private datasets

* *Editor* -- can edit and publish datasets

* *Admin* -- can add, remove and change roles for organization members

.. _finding_data:

Finding data
============

Searching the site
------------------

To find datasets in AGRASTAT, type any combination of search words (e.g. "health",
"transport", etc) in the search box on any page. AGRASTAT displays the first page
of results for your search. You can:

* View more pages of results

* Repeat the search, altering some terms

* Restrict the search to datasets with particular tags, data formats, etc using
  the filters in the left-hand column

If there are a large number of results, the filters can be very helpful, since
you can combine filters, selectively adding and removing them, and modify and
repeat the search with existing filters still in place. Available filters include:

* Business lines

* Impact areas

* Linked value chain

* Countries

* Tags

* Format


If datasets are tagged by geographical area, it is also possible to run AGRASTAT
with an extension which allows searching and filtering of datasets by selecting
an area on a map.

.. image:: /images/search_the_site.jpg


Searching within an organization
--------------------------------

If you want to look for data owned by a particular organization, you can search
within that organization from its home page in AGRASTAT.

#. Select the "Organizations" link at the top of any page.

#. Select the organization you are interested in. AGRASTAT will display your
   organization"s home page.

#. Type your search query in the main search box on the page.

AGRASTAT will return search results as normal, but restricted to datasets from the
organization.

If the organization is of interest, you can opt to be notified of changes to it
(such as new datasets and modifications to datasets) by using the "Follow"
button on the organization page. See the section :ref:`managing_your_news_feed`
below. You must have a user account and be logged in to use this feature.


Exploring datasets
------------------

When you have found a dataset you are interested and selected it, AGRASTAT will
display the dataset page. This includes

* The name, description, and other information about the dataset

* Links to and brief descriptions of each of the resources

.. image:: /images/exploring_datasets.jpg

The resource descriptions link to a dedicated page for each resource. This
resource page includes information about the resource, and enables it to be
downloaded. Many types of resource can also be previewed directly on the
resource page. .CSV and .XLS spreadsheets are previewed in a grid view, with
map and graph views also available if the data is suitable. The resource page
will also preview resources if they are common image types, PDF, or HTML.

The dataset page also has two other tabs:

* *Activity stream* -- see the history of recent changes to the dataset

* *Groups* -- see any group associated with this dataset.

If the dataset is of interest, you can opt to be notified of changes to it by
using the "Follow" button on the dataset page. See the section
:ref:`managing_your_news_feed` below. You must have a user account and be
logged in to use this feature.

.. note::

    If you are a member of an organization, you can also follow the organization
    itself. This will notify you of changes to any dataset owned by the
    organization.


Creating Dashboards
-------------------
AGRASTAT allows the user to create embeddable dashboards from the resources avaibled under their datasets.
To create your dasboard:

#. Find and select the dataset to create the dashboard from

#. From the resources available, select the resource you want to create the dashboard from and Click on "Preview"

#. Click on "New View"

#. Click on "Dashboard View"

#. Provide a title for the dashboard

#. The click on "+" button to add a visual to the dashboard

#. AGRASTAT will ask you to ptovide

    * Title
    * Grid width
    * Type of visual
    * Chart type
    * X-axis
    * Y-axis

#. Once you have provided the information, click on "Save"

#. You can add more visuals to the dashboard by clicking on the "+" button

#. Once you have added all the visuals you need, click on "Add"

.. image:: /images/add_dashboard.jpg



Embedding Dashboards
--------------------
AGRASTAT allows the user to embed created dashboards into websites that support HTML.
To embed your dashboard in other websites, follow the steps below:

#. Navigate to the dashboard you want to embed by previewing the dataset of interest and selecting the dashboard

#. Click on the "Edit view" button

#. Click on the "Embed" button

#. Copy the code provided. You can set the height and width of the dashboard to fit your website.


.. image:: /images/embed_dashboard.jpg


Exploring FAOSTAT datasets
--------------------------

AGRASTAT supports exploring data fro FAOSTAT. 


To explore FAOSTAT datasets, use the "Resources" link at the top of any page and select "FAOSTAT". 

.. image:: /images/resources.jpg


Filter the dataset as needed to view or download

.. image:: /images/explore_faostat.jpg


Search in detail
================

AGRASTAT supports two search modes, both are used from the same search field.
If the search terms entered into the search field contain no colon (":")
AGRASTAT will perform a simple search. If the search expression does contain at
least one colon (":") AGRASTAT will perform an advanced search.

Simple Search
-------------

AGRASTAT defers most of the search to Solr and by default it uses the `DisMax Query
Parser <https://lucene.apache.org/solr/guide/6_6/the-dismax-query-parser.html>`_
that was primarily designed to be easy to use and to accept almost any input
without returning an error.

The search words typed by the user in the search box defines the main "query"
constituting the essence of the search. The + and - characters are
treated as **mandatory** and **prohibited** modifiers for terms. Text wrapped
in balanced quote characters (for example, "San Jose") is treated as a phrase.
By default, all words or phrases specified by the user are treated as
**optional** unless they are preceded by a "+" or a "-".

.. note::

    AGRASTAT will search for the **complete** word and when doing simple search are
    wildcards are not supported.

Simple search examples:

* ``census`` will search for all the datasets containing the word "census" in
  the query fields.

* ``census +2019`` will search for all the datasets contaning the word "census"
  and filter only those matching also "2019" as it is treated as mandatory.

* ``census -2019`` will search for all the datasets containing the word
  "census" and will exclude "2019" from the results as it is treated as
  prohibited.

* ``"european census"`` will search for all the datasets containing the phrase
  "european census".

Solr applies some preprocessing and stemming when searching. Stemmers remove
morphological affixes from words, leaving only the word stem. This may cause,
for example, that searching for "testing" or "tested" will show also results
containing the word "test".

* ``Testing`` will search for all the datasets containing the word "Testing"
  and also "Test" as it is the stem of "Testing".

.. note::

    If the Name of the dataset contains words separated by "-" it will consider
    each word independently in the search.


Advanced Search
---------------

If the query has a colon in it it will be considered a fielded search and the
query syntax of Solr will be used to search. This will allow us to use wildcards
"*", proximity matching "~" and general features described in Solr docs.
The basic syntax is ``field:term``.

Advanced Search Examples:

* ``title:european`` this will look for all the datasets containing in its
  title the word "european".

* ``title:europ*`` this will look for all the datasets containing in its title
  a word that starts with "europ" like "europe" and "european".

* ``title:europe || title:africa`` will look for datasets containing "europe"
  or "africa" in its title.

* ``title: "european census" ~ 4`` A proximity search looks for terms that
  are within a specific distance from one another. This example will look for
  datasets which title contains the words "european" and "census" within a
  distance of 4 words.

* ``author:powell~`` AGRASTAT supports fuzzy searches based on the Levenshtein
  Distance, or Edit Distance algorithm. To do a fuzzy search use the "~"
  symbol at the end of a single-word term. In this example words like
  "jowell" or "pomell" will also be found.


.. note::

    Field names used in advanced search may differ from Datasets Attributes,
    the mapping rules are defined in the ``schema.xml`` file. You can use ``title``
    to search by the dataset name and ``text`` to look in a catch-all field that
    includes author, license, mantainer, tags, etc.

.. note::

    AGRASTAT uses Apache Solr as its search engine. For further details check the
    `Solr documentation
    <https://lucene.apache.org/solr/guide/6_6/searching.html#searching>`_.
    Please note that AGRASTAT sometimes uses different values than what is mentioned
    in that documentation. Also note that not the whole functionality is offered
    through the simplified search interface in AGRASTAT or it can differ due to
    extensions or local development in your AGRASTAT instance.


Personalization
===============

AGRASTAT provides features to personalize the experience of both searching for and
publishing data. You must be logged in to use these features.

.. _managing_your_news_feed:

Managing your news feed
-----------------------

At the top of any page, select the dashboard symbol (next to your name). AGRASTAT
displays your News feed. This shows changes to datasets that you follow, and
any changed or new datasets in organizations that you follow. The number by the
dashboard symbol shows the number of new notifications in your News feed since
you last looked at it. As well as datasets and organizations, it is possible to
follow individual users (to be notified of changes that they make to datasets).

.. image:: /images/manage_news_feed.jpg

If you want to stop following a dataset (or organization or user), go to the
dataset"s page (e.g. by selecting a link to it in your News feed) and select
the "Unfollow" button.

Managing your user profile
--------------------------

You can change the information that AGRASTAT holds about you, including what other
users see about you by editing your user profile. (Users are most likely to see
your profile when you edit a dataset or upload data to an organization that
they are following.) To do this, select the gearwheel symbol at the top of any
page.

.. image:: /images/manage_user_profile.jpg

AGRASTAT displays the user settings page. Here you can change:

* Your username

* Your full name

* Your e-mail address (note: this is not displayed to other users)

* Your profile text - an optional short paragraph about yourself

* Your password

Make the changes you require and then select the "Update Profile" button.

.. note::

    If you change your username, AGRASTAT will log you out. You will need to log
    back in using your new username.


Data converter
==================
Purpose of the Data converter
-----------------------------
This tool allows users to upload and convert Excel (.xlsx) and Stata (.dta) files into CSV format.

Steps to use the Data converter
-------------------------------
* Navigate to the Converter Page: Ensure you are on the Converter page on the AgraStat website.

* Upload the File: Click the Choose files button.Select either an Excel (.xlsx) or Stata (.dta) file from your computer that you want to convert. The file name will appear next to the Choose files button once selected.

* Required Field:T he system marks the file upload field as required. Ensure that a file is selected before proceeding.

* Convert the File: After selecting the file, click the green button labeled Convert to CSV. The system will process your file and convert it into CSV format.

* Download the Converted File: Once the conversion is complete, a link to download the converted CSV file will be available.

Feel free to repeat this process for any additional files you wish to convert.

.. image:: /images/data_converter.jpg


Dataset statistics
==================
Understanding the Dataset Statistics
-------------------------------------
The Dataset Statistics provides a visual representation of dataset distribution across different countries, business lines, and value chains. 
This page helps users quickly analyze dataset availability and focus areas.

* Top 10 Countries - This section lists the top 10 countries based on the number of datasets available. The dataset count for each country, allows users to compare dataset availability across different regions.

* Business Lines Dataset - A radar chart representing the distribution of datasets across different business lines. 

* Value Chains Dataset - A radar chart illustrating dataset distribution across various agricultural value chains. Each category represents a specific crop or product, with dataset counts shown in brackets.

* Top Users by Dataset Count - This section lists the users who have uploaded the most datasets. Example: "admin" has uploaded 3 datasets, making them the top contributor.

* Top Datasets by Followers - This section highlights the datasets that are being followed the most by users on the platform. Example: "Example Kobo Data" has the highest interest with 3 followers.

* Top Datasets by Views - This section displays how many times each dataset has been viewed by users.

.. image:: /images/dataset_statistics.jpg


Getting in touch
================

Contact
--------
Contact page is designed to help you reach out to the support team quickly and efficiently. 
Whether you have questions, feedback, or need assistance.

To use the contact page, use the "Resources" link at the top of any page and select "Contact".

.. image:: /images/contact_us_1.jpg

AGRASTAT will ask for the following:

* Contact Email 

* Contact Name

* Subject 

* Business Line 

* Message

.. image:: /images/contact_us_2.jpg

Once all required fields are filled, click the Submit button to send your inquiry. You should receive a confirmation that your message has been sent.