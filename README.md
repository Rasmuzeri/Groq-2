Clone the project.
## Install dependencies
### Backend
First, install Python and Pip. Then, in the root folder:
```
pip install fastapi uvicorn transformers python-dotenv requests groq
```
Also, put in your Groq and Hugging Face API keys.
### Frontend
Install Node.js. Open the sentiment-ui folder.

Install the frontend dependencies:
```
npm install axios react-icons
```
## Running
### Run backend from root
```
uvicorn app:app --reload
```
### Run frontend from /sentiment-ui
```
npm run dev
```
Open the frontend URL that is provided in the console.
## Usage
1. Write your sentiment in the text box.
2. Pick the model from the dropdown menu.
3. Click "Analyze Sentiment".
