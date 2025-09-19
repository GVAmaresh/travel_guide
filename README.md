# TravelHues AI Agent

Welcome to the TravelHues AI Agent project! This is a sophisticated conversational AI assistant designed to help users plan their travel itineraries. The agent is powered by Google's Gemini Pro model via Vertex AI and uses Firestore and Vector Search for long-term memory and context.


### Architecture Overview

The system is built around a few core components:

* **FastAPI Backend:** A Python web server that exposes the agent's capabilities through a secure REST API.
* **Trip Planner Agent:** The core logic unit that uses the Gemini model and a state machine to manage conversations and gather user requirements.
* **Firestore Database:** Used as the primary data store for user profiles (e.g., preferences) and conversation history.
* **Vertex AI Vector Search:** Provides long-term semantic memory, allowing the agent to recall conceptually similar past conversations.
* **Google Cloud Function:** An event-driven, serverless function that automatically updates the Vector Search index whenever a new conversation is saved to Firestore.


###  Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Python 3.10+**
2.  **Google Cloud SDK (`gcloud` CLI):** [Installation Guide](https://cloud.google.com/sdk/docs/install)
3.  **Google Cloud Project:** You need access to a GCP project with the following APIs enabled:
    * Vertex AI API
    * Cloud Firestore API
    * Cloud Functions API
    * Cloud Run API (for deploying the API server later)


### Local Development Setup

Follow these steps to set up and run the project on your local machine.

#### 1. Clone the Repository

```bash
git clone https://github.com/GVAmaresh/travel_guide
cd travel_guide
```

#### 2. Set Up the Python Environment

Create and activate a Python virtual environment to keep dependencies isolated.

```bash
python3 -m venv venv

source venv/bin/activate
```

#### 3. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the root of the project by copying the example.

```bash
cp .env.example .env
```

Now, edit the `.env` file with your specific configuration:

```env
GCP_PROJECT_ID="your-gcp-project-id-here"
JWT_SECRET_KEY="generate-a-long-random-secret-string-for-jwt"
```

#### 5. Authenticate with Google Cloud

Run the following commands in your terminal to log in and configure the SDK. This allows your local application to securely access Google Cloud services.

```bash
gcloud auth login

gcloud config set project your-gcp-project-id-here

gcloud auth application-default login
```

---

### Running the Application Locally

Once the setup is complete, you can run the FastAPI web server.

1. **Start the Server:**

    ```bash
    uvicorn src.api.main:app --reload
    ```

    * `src.api.main`: The Python path to your main file.
    * `app`: The `app = FastAPI()` object inside that file.
    * `--reload`: Enables auto-reload for development, so the server restarts when you save code changes.

2.  **Access the API:** 
    - The server will be running on `http://127.0.0.1:8000`. 
    - In future you can access the interactive API documentation (Swagger UI) at **`http://127.0.0.1:8000/docs`**.

---

### Deploying Cloud Components

#### Deploying the Vector Update Function

The Cloud Function that keeps your Vector Search index up-to-date must be deployed separately.

Run this command from the root of your project directory. Ensure the `--source` directory contains the function's `main.py` and its `requirements.txt`.

```bash
gcloud functions deploy update_vector_memory \
--gen2 \
--runtime python311 \
--project YOUR_GCP_PROJECT_ID \
--region us-central1 \
--source ./path/to/your/function/code \
--entry-point update_vector_memory \
--trigger-event-filters="type=google.cloud.firestore.document.v1.written" \
--trigger-event-filters="database=(default)" \
--trigger-event-filters-path-pattern="document=conversations/{userId}"
```

-----

## Postman Guide 



### Part 1: Authentication

#### Step 1: Register User

  * **Endpoint:** `POST /register`
  * **Body (JSON):**
    ```json
    {
        "username": "testuser",
        "password": "testpass"
    }
    ```
  * **Result:** A success message.

#### Step 2: Get Token

  * **Endpoint:** `POST /token`
  * **Body (x-www-form-urlencoded):**
      * `username`: `testuser`
      * `password`: `testpass`
  * **Action (in "Tests" tab):** Save the token.
    ```javascript
    pm.collectionVariables.set("JWT", pm.response.json().access_token);
    ```
  * **Result:** An access token is saved to `{{JWT}}`.

-----

### Part 2: Planning & Flights

**(Setup: Go to your collection's "Authorization" tab, select "Bearer Token", and put `{{JWT}}` in the Token field.)**

#### Step 3: Start a New Plan

  * **Endpoint:** `POST /plan-trip`

  * **Body (JSON) - Choose one option:**

      * **Option 1 (Fixed Dates):**
        ```json
        {
            "origin": "Bangalore",
            "destination": "Bali",
            "is_flexible": false,
            "dates": {
                "start_date": "2025-10-11",
                "end_date": "2025-10-17"
            },
            "include_flights": true
        }
        ```
      * **Option 2 (Flexible Dates):**
        ```json
        {
            "origin": "Bangalore",
            "destination": "Bali",
            "is_flexible": true,
            "dates": {
                "month": "October",
                "days": "7"
            },
            "include_flights": true
        }
        ```

  * **Action (in "Tests" tab):** Save the session ID.

    ```javascript
    pm.collectionVariables.set("session_id", pm.response.json().session_id);
    ```

  * **Result:** The AI's analysis, suggested dates (if flexible), and a `session_id` are returned and saved.
Of course. Here is the updated section for your Postman guide, reflecting the change to a `POST` request.


#### Step 4: Get Flight Options

  * **Endpoint:** `POST /get-flights`
  * **Body (JSON):**
    ```json
    {
        "session_id": "{{session_id}}"
    }
    ```
  * **Result:** A list of "best" and "budget" flight options.
  * **Action:** From the response, **manually copy** the `flight_id` for your chosen onward and return flights for the next step.

#### Step 5: Confirm Your Flights

  * **Endpoint:** `POST /confirm-flights`
  * **Body (JSON):** Paste the `flight_id` values you copied.
    ```json
    {
        "session_id": "{{session_id}}",
        "onward_flight": "SQ-511-SQ-944",
        "return_flight": "OD-242-OD-177"
    }
    ```
  * **Result:** A success message. The selected flights are now saved to your session.

-----

### Part 3: Finalize the Plan

#### Step 6: Generate Trip Summary

  * **Endpoint:** `POST /generate-summary`
  * **Body (JSON):** Provide your preferences. The AI will use these **and your confirmed flight details** to create the summary.
    ```json
    {
        "session_id": "{{session_id}}",
        "preferences": {
            "budget": "Standard",
            "theme": ["Adventure & Nature"],
            "food_preferences": ["Local Cuisine"],
            "traveling_with": "Partner"
        },
        "additional_details": "We want a mix of adventure and relaxation."
    }
    ```
  * **Result:** A human-readable summary of your complete trip plan for review.

#### Step 7: Confirm the Summary

  * **Endpoint:** `POST /update-summary`

  * **Body (JSON) - Choose one action:**

      * **To Confirm:**
        ```json
        {
            "session_id": "{{session_id}}",
            "action": "confirm"
        }
        ```
      * **To Edit:**
        ```json
        {
            "session_id": "{{session_id}}",
            "action": "edit",
            "edited_summary_text": "I want to visit Bali from Oct 11 to 17. The confirmed flight is Singapore Airlines. We want an adventurous trip with a focus on local food."
        }
        ```

  * **Final Result:** You get the final, detailed prompt. This prompt contains **all the confirmed details** (dates, flights, preferences) ready to be sent to another AI to generate the final day-by-day itinerary.