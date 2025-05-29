<h1>Software-Engineering-Project-24-25</h1>
<h3>Software engineering project of the CEID undergraduate course "Software Technology".</h3>

The application titled CaRent is a web-based, peer-to-peer vehicle rental system. It supports two types of users: regular users and administrators.

Regular users can create an account and log into the system. Once logged in, the system welcomes the user with a map of their local area. The user sees pins on the map representing rental listings. They can search based on location and apply filters so that only listings of interest are displayed. A similar feature is available in the listings menu, where users can search for specific vehicles using filters.

Whether the user searches via the map or the listings menu, selecting a specific listing leads to its detailed description, from which the user can submit a rental request. If the user chooses to rent the vehicle, a notification is sent to the vehicle’s owner. Any owner can upload their vehicle to the system for rental. If the owner accepts the request, the transaction is completed.

The application takes a commission from the owners upon each transaction, unless they have chosen a subscription package. This package requires a small monthly fee and results in either no commission or a reduced one.

All users can edit or cancel the listings they have uploaded, as well as rate or report vehicle rentals from other owners with whom they’ve previously interacted. Additionally, all users can edit their account details.

Administrators have the ability to view user rental statistics and export them as files. They can also review user reports, deactivate malicious accounts if necessary, and issue refunds.

To start the app run the script code/app/main.py
