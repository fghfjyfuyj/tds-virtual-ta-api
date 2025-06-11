import requests
import json # Import the json library for pretty printing

def scrape_discourse(base_url, start_date, end_date):
    # TODO: Replace "YOUR_DISCOURSE_API_TOKEN" with your actual API token
    headers = {"Authorization": "Bearer YOUR_DISCOURSE_API_TOKEN"}
    posts = []
    for page in range(1, 5):  # Adjust the range as needed
        url = f"{base_url}/posts?page={page}"
        print(f"Attempting to fetch URL: {url}") # Add print statement to show the URL being fetched
        response = requests.get(url, headers=headers)
        print(f"Response status code: {response.status_code}") # Add print statement to show the status code

        if response.status_code == 200:
            try:
                # Attempt to parse JSON
                data = response.json()
                # Print the first few characters of the response text if JSON parsing fails
                # to help diagnose the issue.
                print("Successfully parsed JSON.")
                # Optionally, print the raw response text or parsed data for debugging
                # print("Response Text:")
                # print(response.text[:500]) # Print first 500 characters
                # print("Parsed Data:")
                # print(json.dumps(data, indent=2)[:500]) # Print first 500 characters of pretty-printed JSON

                # Check if the response is a list and not empty
                if isinstance(data, list) and data:
                    for post in data:
                        # Add checks for expected keys in the post dictionary
                        if all(key in post for key in ['created_at', 'topic_title', 'cooked', 'url']):
                            if start_date <= post['created_at'] <= end_date:
                                posts.append({
                                    "title": post['topic_title'],
                                    "content": post['cooked'],
                                    "url": post['url']
                                })
                        else:
                            print(f"Skipping post due to missing keys: {post}")
                elif isinstance(data, dict) and data:
                     print("Response is a dictionary, not a list of posts as expected.")
                     print(f"Response content (first 500 chars): {response.text[:500]}")
                else:
                    print("Response is empty or not in the expected format (list).")
                    print(f"Response content (first 500 chars): {response.text[:500]}")

            except requests.exceptions.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
                print("Response text content:")
                print(response.text) # Print the full response text if JSON decoding fails
                # Stop processing for this page as it's not the expected format
                break # Exit the loop for this page if JSON parsing fails
            except Exception as e:
                print(f"An unexpected error occurred while processing response: {e}")
                print("Response text content:")
                print(response.text) # Print the full response text for other errors
                 # Stop processing for this page
                break

        elif response.status_code == 401:
             print("Authentication failed. Check your API token.")
             print("Response text content:")
             print(response.text)
             break # Stop processing if authentication fails

        elif response.status_code >= 400:
            print(f"HTTP error occurred: {response.status_code}")
            print("Response text content:")
            print(response.text)
            # Decide whether to break or continue based on the expected behavior
            # break # Uncomment to stop on any HTTP error

    return posts

# URL to scrape
# TODO: Replace "YOUR_DISCOURSE_API_TOKEN" with your actual API token
posts = scrape_discourse("https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34/l/top?period=quarterly", "2025-01-01", "2025-04-14")
