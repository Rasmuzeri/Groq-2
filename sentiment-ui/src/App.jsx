import { useState } from 'react';
import axios from 'axios';
import { FaSpinner, FaCheck, FaTimes } from 'react-icons/fa';
import './App.css'; // Regular CSS file

const API_URL = 'http://localhost:8000/analyze/';

export default function App() {
  const [text, setText] = useState('');
  const [model, setModel] = useState('custom');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      setError('Please enter some text');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      const response = await axios.post(API_URL, {
        text: text.trim(),
        model
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <h1 className="app-title">Sentiment Analysis</h1>
        
        <div className="input-section">
          <label className="input-label">
            Enter Text
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="text-input"
            rows="4"
            placeholder="Enter your text here..."
          />
        </div>

        <div className="controls-container">
          <div className="model-selector">
            <label className="input-label">
              Select Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="model-dropdown"
            >
              <option value="custom">Custom Model</option>
              <option value="llama">Llama 3</option>
            </select>
          </div>

          <div className="button-container">
            <button
              onClick={analyzeSentiment}
              disabled={loading}
              className="analyze-button"
            >
              {loading ? (
                <>
                  <FaSpinner className="spinner-icon" />
                  Analyzing...
                </>
              ) : (
                'Analyze Sentiment'
              )}
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <FaTimes className="error-icon" />
            {error}
          </div>
        )}

        {result && (
          <div className="result-container">
            <h2 className="result-title">Results:</h2>
            <div className="result-content">
              <span className={`sentiment-text ${result.sentiment}`}>
                {result.sentiment}
              </span>
              <div className="confidence-meter">
                <div className="confidence-bar" style={{ width: `${result.confidence * 100}%` }} />
                <span className="confidence-text">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}