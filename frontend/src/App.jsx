import "./App.css";
import { useState, useEffect } from "react";

function App() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    const savedFiles = JSON.parse(localStorage.getItem("uploadedFiles")) || [];
    setFiles(savedFiles);
  }, []);

  function handleFileChange(event) {
    const selectedFiles = Array.from(event.target.files);

    const newFiles = selectedFiles.map((file) => ({
      name: file.name,
      size: file.size,
      type: file.type
    }));

    const updatedFiles = [...files, ...newFiles];

    setFiles(updatedFiles);
    localStorage.setItem("uploadedFiles", JSON.stringify(updatedFiles));
  }

  function removeFile(index) {
    const updatedFiles = files.filter((_, i) => i !== index);

    setFiles(updatedFiles);
    localStorage.setItem("uploadedFiles", JSON.stringify(updatedFiles));
  }

  function resetFiles() {
    setFiles([]);
    localStorage.removeItem("uploadedFiles");
  }

  return (
    <div className="container">
      <div className="header">
        <h1>TechSmiths</h1>
        <p>Multi-Source Document Intelligence</p>
      </div>

      <div className="section">
        <h2>Upload Documents</h2>

        <input
          type="file"
          multiple
          onChange={handleFileChange}
        />

        {files.length > 0 && (
          <div>
            <h3>Uploaded Documents</h3>

            <ul className="sources">
              {files.map((file, index) => (
                <li key={index}>
                  {file.name}
                  <button
                    className="remove-button"
                    onClick={() => removeFile(index)}
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>

            <button
              className="reset-button"
              onClick={resetFiles}
            >
              Reset All
            </button>
          </div>
        )}
      </div>

      <div className="section">
        <h2>Ask a Question</h2>

        <div className="question-box">
          <input
            type="text"
            placeholder="Ask something about your documents..."
          />
          <button>Ask</button>
        </div>
      </div>

      <div className="section">
        <h2>Answer</h2>

        <div className="answer">
          Your verified answer will appear here.
        </div>
      </div>

      <div className="section">
        <h2>Sources</h2>

        <ul className="sources">
          <li>Document sources will appear here.</li>
        </ul>
      </div>

      <div className="section">
        <h2>Conflicts</h2>

        <div className="conflict">
          Detected conflicts will appear here.
        </div>
      </div>

      <button>Generate Verified Report</button>
    </div>
  );
}

export default App;