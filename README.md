<img src="logo.png" alt="Description of logo" width="300" />

# Welcome to Shortify API! 

This powerful tool allows you to create, manage, and track short URLs for your marketing campaigns. By using Shortify API, you can generate customizable and trackable links that enhance your marketing effectiveness. These short URLs can even be used to generate QR codes, making them versatile for both digital and offline campaigns. Whether you're hosting the service locally or deploying it to the cloud, this guide will help you get started.

## Key Benefits

- **Trackable URLs**: Gain valuable insights into user engagement by monitoring click logs.
- **Customizable Links**: Create short links that align with your branding.
- **QR Code Compatibility**: Easily convert your short URLs into QR codes for offline campaigns.
- **Flexible Deployment**: Host the API locally, on a web server, or in a cloud environment using Docker or proxies like NGINX.

## Getting Started

### 1. Prerequisites

Ensure the following tools are installed on your machine:

- Python 3.8 or higher
- pip (Python package installer)
- Postman (for API testing, optional)

### 2. Installation

1. Clone the repository or download the source code.
2. Navigate to the directory containing the `app.py` file.
3. Install the required Python libraries:
   ```bash
   pip install flask flask-cors


Run the backend service:
python app.py

By default, Flask will start the service at http://localhost:5000.

API Documentation
Base URL
The API assumes a base URL of http://localhost:5000. Replace this with your deployment URL if hosting externally.
Available Endpoints


Create Short Link

Endpoint: /create
Method: POST
Headers:
{
  "Content-Type": "application/json"
}


Body:
{
  "project_name": "My Project",
  "destination_url": "https://example.com"
}





Redirect to Destination

Endpoint: /{unique_id}
Method: GET
Description: Redirects to the destination URL associated with the unique ID.



Get Redirect Logs

Endpoint: /logs/{unique_id}
Method: GET
Description: Retrieves logs for clicks on a specific short link.



Get All Redirect Logs

Endpoint: /logs/0
Method: GET
Description: Retrieves logs for all short links.



Get All Short Links

Endpoint: /all_links
Method: GET
Description: Returns all the short links created.



Update Short Link

Endpoint: /update/{unique_id}
Method: PUT
Headers:
{
  "Content-Type": "application/json"
}


Body:
{
  "project_name": "Updated Project",
  "destination_url": "https://updated-example.com"
}





Delete Short Link

Endpoint: /delete/{unique_id}
Method: DELETE



Testing the API
Use Postman to interact with the API:

Import the provided Postman collection (ShortifyAPI_PostmanCollection.json).
Test the endpoints using the included sample requests.
Replace localhost with your custom URL when deploying to a server.

Example Frontend Integration
The frontend.py file demonstrates how to interact with the API programmatically. While this is a basic example, it can be expanded to suit your application's needs. Make sure the required imports are included:
import requests

To run the frontend example, install the requests library:
pip install requests

Deployment Recommendations

Web Server: Deploy using NGINX, Apache, or any preferred web server.
Cloud Hosting: Use platforms like AWS, Azure, or Google Cloud.
Proxy Setup: Employ Cloudflare Tunnels or similar services for secure access.
Containerization: Use Docker for easy setup and scalability.

Contact and Support
If you have any issues or questions, feel free to reach out via the project repository or community forums.
Enjoy using Shortify API to elevate your marketing efforts!
© 2025 ShortifyAPI – https://davidsoden.com

Is there anything else you would like to do with this document?

