import React, { useState } from "react";
import axios from "axios";
import './App.css';

function App() {
  const API_URL = "https://result-fast-api.onrender.com";
  const [file, setFile] = useState(null);
  const [columns, setColumns] = useState([]);
  const [selectedCol, setSelectedCol] = useState("");
  const [uniqueValues, setUniqueValues] = useState([]);
  const [selectedVal, setSelectedVal] = useState("");
  const [count, setCount] = useState(null);
  const [summary, setSummary] = useState(null);
  const [gradeCols, setGradeCols] = useState([]);
  const [gradeSummaryFull, setGradeSummaryFull] = useState([]);
  const [grades, setGrades] = useState([]);
  const [counts, setCounts] = useState([]);
  const [topper, setTopper] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Please select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_URL}/upload_csv`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const sem_overall_grades_res = await axios.get(`${API_URL}/overall_summary`);
      const summaryRes = await axios.get(`${API_URL}/gradesummary_full`);
      const gradeRes = await axios.get(`${API_URL}/grades`);
      const topper = await axios.get(`${API_URL}/class_topper`);

      setGradeSummaryFull(summaryRes.data.summary || []);
      setGrades(sem_overall_grades_res.data.grades || []);
      setCounts(sem_overall_grades_res.data.counts || []);
      setColumns(res.data.columns || []);
      setSummary(res.data.summary || null);
      setTopper(topper.data || []);
      setGradeCols(gradeRes.data.grade_columns || []);
    } catch (err) {
      console.error(err);
      alert('Upload failed. Check console for details.');
    }
  };

  const handleColumnSelect = async (col) => {
    setSelectedCol(col);
    setSelectedVal("");
    setCount(null);
    try {
      const res = await axios.get(`${API_URL}/unique/${col}`);
      setUniqueValues(res.data.unique_values || []);
    } catch (err) {
      console.error(err);
      setUniqueValues([]);
    }
  };

  const handleValueSelect = async (val) => {
    setSelectedVal(val);
    try {
      const res = await axios.get(
        `${API_URL}/count/${selectedCol}/${encodeURIComponent(val)}`
      );
      setCount(res.data.count);
    } catch (err) {
      console.error(err);
      setCount(null);
    }
  };

  return (
    <div className="page-root">
      <header className="header">
        <h1>Result Analyzer</h1>
      </header>

      <main className="container">
        <section className="uploader">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            className="file-input"
          />
          <button onClick={handleUpload} className="btn primary">Upload</button>
        </section>

        {summary && summary.total_students && (
          <section className="summary-card">
            <h2>Exam Summary</h2>
            <div className="summary-grid">
              <div>
                <div className="summary-value">{summary.total_students}</div>
                <div className="summary-label">Total Students</div>
              </div>
              <div>
                <div className="summary-value">{summary.passed_students}</div>
                <div className="summary-label">Passed Students</div>
              </div>
              <div>
                <div className="summary-value">{summary.pass_percentage}%</div>
                <div className="summary-label">Pass %</div>
              </div>
            </div>
          </section>
        )}

        {
          <div className="topper-card">
  <h2>🏆 Class Topper</h2>
  {topper ? (
    <div className="topper-info">
      <p><span>Name:</span> {topper.name}</p>
      <p><span>Register No:</span> {topper.register_number}</p>
      <p><span>Total Marks:</span> {topper.total_marks}</p>
      <p><span>Overall Grade:</span> {topper.overall_grade}</p>
    </div>
  ) : (
    <p className="muted">No topper data available.</p>
  )}
</div>
        }

        {columns.length > 0 && (
          <section className="controls">
            <label className="label">Select Column</label>
            <select
              value={selectedCol}
              onChange={(e) => handleColumnSelect(e.target.value)}
              className="select"
            >
              <option value="">--Choose Column--</option>
              {gradeCols.map((col, idx) => (
                <option key={idx} value={col}>{col}</option>
              ))}
            </select>

            {uniqueValues.length > 0 && (
              <>
                <label className="label">Select Value</label>
                <select
                  value={selectedVal}
                  onChange={(e) => handleValueSelect(e.target.value)}
                  className="select"
                >
                  <option value="">--Choose Value--</option>
                  {uniqueValues.map((val, idx) => (
                    <option key={idx} value={val}>{val}</option>
                  ))}
                </select>
              </>
            )}

            {count !== null && (
              <div className="count-box"><b>{count}</b> students secured <strong>{selectedVal}</strong> in <strong>{selectedCol}</strong></div>
            )}
          </section>
        )}

        <section className="card">
          <h2>🎓 Semester Overall Grade Summary</h2>

          {grades.length > 0 ? (
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Grade</th>
                    {grades.map((grade, i) => <th key={i}>{grade}</th>)}
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="label-cell">Count</td>
                    {counts.map((c, i) => <td key={i}>{c}</td>)}
                  </tr>
                </tbody>
              </table>
            </div>
          ) : (
            <p className="muted">No overall data available yet.</p>
          )}
        </section>

        {gradeCols.length > 0 && (
          <section className="card">
            {gradeSummaryFull.length > 0 ? (
              <>
                <h2>📊 Subject Performance Overview</h2>
                <div className="table-wrap">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Subject</th>
                        <th>Passed</th>
                        <th>Pass %</th>
                        <th>Topper Name</th>
                        <th>Register No.</th>
                        <th>Marks</th>
                        <th>Grade</th>
                      </tr>
                    </thead>
                    <tbody>
                      {gradeSummaryFull.map((item, idx) => (
                        <tr key={idx}>
                          <td className="subject-cell">{item.subject}</td>
                          <td>{item.passed_students}</td>
                          <td>{item.pass_percentage}%</td>
                          <td>{item.topper ? item.topper.name : 'N/A'}</td>
                          <td>{item.topper ? item.topper.register_number : 'N/A'}</td>
                          <td>{item.topper ? item.topper.marks : 'N/A'}</td>
                          <td>{item.topper ? item.topper.grade : 'N/A'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            ) : (
              <p className="muted">No subject performance data available yet.</p>
            )}
          </section>
        )}

      </main>

      <footer className="footer">Developed by Ms. Soumya Koshy</footer>
    </div>
  );
}

export default App;

