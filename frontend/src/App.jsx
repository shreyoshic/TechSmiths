import "./App.css";
import { useEffect, useState } from "react";

function App() {
  const [files, setFiles] = useState([]);
  const [question, setQuestion] = useState("");
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    const savedFiles = JSON.parse(
      localStorage.getItem("uploadedFiles") || "[]"
    );

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

    event.target.value = "";
  }

  function removeFile(index) {
    const updatedFiles = files.filter((_, i) => i !== index);

    setFiles(updatedFiles);
    localStorage.setItem("uploadedFiles", JSON.stringify(updatedFiles));
  }

  function resetFiles() {
    setFiles([]);
    localStorage.removeItem("uploadedFiles");
    setShowResults(false);
  }

  function handleAsk() {
    if (!question.trim()) {
      return;
    }

    setShowResults(true);
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>VeriTrace</h1>
          <p>Evidence-grounded, not just AI-generated.</p>
        </div>
      </header>

      <main className="container">

        <section className="section upload-section">
          <div className="section-title">
            <div>
              <h2>Upload Documents</h2>
              <p>
                Add reports, manuals, logs, and other source documents.
              </p>
            </div>
          </div>

          <label className="upload-box">
            <input
              type="file"
              multiple
              onChange={handleFileChange}
            />

            <span className="upload-icon">+</span>

            <strong>Choose documents</strong>

            <span>
              PDF, TXT and LOG files supported
            </span>
          </label>

          {files.length > 0 && (
            <div className="file-list-container">
              <div className="file-list-header">
                <h3>Uploaded Documents</h3>

                <button
                  className="reset-button"
                  onClick={resetFiles}
                >
                  Reset All
                </button>
              </div>

              <div className="file-list">
                {files.map((file, index) => (
                  <div className="file-item" key={`${file.name}-${index}`}>
                    <div className="file-info">
                      <span className="file-icon">PDF</span>

                      <div>
                        <strong>{file.name}</strong>

                        <span>
                          {(file.size / 1024).toFixed(1)} KB
                        </span>
                      </div>
                    </div>

                    <button
                      className="remove-button"
                      onClick={() => removeFile(index)}
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>


        <section className="section">
          <div className="section-title">
            <div>
              <h2>Ask a Question</h2>
              <p>
                Ask something about the uploaded evidence.
              </p>
            </div>
          </div>

          <div className="question-box">
            <input
              type="text"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  handleAsk();
                }
              }}
              placeholder="What temperature readings were reported for MX-01?"
            />

            <button
              className="ask-button"
              onClick={handleAsk}
            >
              Ask
            </button>
          </div>
        </section>


        {showResults && (
          <>
            <section className="section">
              <div className="section-title">
                <div>
                  <h2>Answer</h2>
                  <p>Evidence-grounded response</p>
                </div>

                <span className="verified-badge">
                  Verified Evidence
                </span>
              </div>

              <div className="answer">
                <p>
                  MX-01 was reported at two different temperatures:
                </p>

                <div className="temperature-values">
                  <span>72°C</span>
                  <span>91°C</span>
                </div>

                <p>
                  The two source documents contain conflicting
                  temperature readings for the same machine.
                </p>
              </div>
            </section>


            <section className="section">
              <div className="section-title">
                <div>
                  <h2>Sources</h2>
                  <p>Evidence used to produce the answer</p>
                </div>
              </div>

              <div className="source-card">
                <div className="source-top">
                  <strong>Inspection_Report.pdf</strong>
                  <span>Page 1</span>
                </div>

                <p>
                  Measured Operating Temperature: <strong>72°C</strong>
                </p>
              </div>

              <div className="source-card">
                <div className="source-top">
                  <strong>Technician_Log.pdf</strong>
                  <span>Page 1</span>
                </div>

                <p>
                  Observed Temperature: <strong>91°C</strong>
                </p>
              </div>

              <div className="source-card">
                <div className="source-top">
                  <strong>Machine_Manual.pdf</strong>
                  <span>Page 1</span>
                </div>

                <p>
                  Recommended operating temperature:
                  <strong> 60–75°C</strong>
                </p>
              </div>
            </section>


            <section className="section">
              <div className="section-title">
                <div>
                  <h2>Conflicts</h2>
                  <p>Detected inconsistencies between sources</p>
                </div>

                <span className="conflict-badge">
                  1 Conflict
                </span>
              </div>

              <div className="conflict">
                <div className="conflict-header">
                  <strong>Temperature Conflict</strong>
                  <span>CONFLICT</span>
                </div>

                <p>
                  Multiple sources report different temperatures
                  for the same machine.
                </p>

                <div className="conflict-values">
                  <div>
                    <strong>72°C</strong>
                    <span>Inspection Report</span>
                  </div>

                  <div>
                    <strong>91°C</strong>
                    <span>Technician Log</span>
                  </div>
                </div>

                <p className="conflict-note">
                  VeriTrace does not arbitrarily choose one value.
                  Both source claims are preserved for verification.
                </p>
              </div>
            </section>


            <section className="section report-section">
              <div>
                <h2>Verified Report</h2>

                <p>
                  Generate a consolidated report containing the
                  answer, supporting sources, and detected conflicts.
                </p>
              </div>

              <button className="report-button">
                Generate Verified Report
              </button>
            </section>
          </>
        )}

      </main>
    </div>
  );
}

export default App;