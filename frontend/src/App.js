import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState({
    count: 0,
    status: "Loading..."
  });

  useEffect(() => {
    const fetchData = () => {
      fetch("http://127.0.0.1:8000/status/")
        .then(res => res.json())
        .then(data => setData(data))
        .catch(err => console.error(err));
    };

    fetchData();

    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Metro Crowd Status</h1>
      <h2>People Count: {data.count}</h2>
      <h2>Status: {data.status}</h2>
    </div>
  );
}

export default App;