import { useState } from "react";
import axios from "axios";
import { headers } from "next/headers";




export default function Home() {

  const [file, setFile] = useState<File | null>(null);
  const [progress,setProgress]=useState({started:false,pc:0});
  const [msg, setMsg] = useState<string | null>(null);
    
    function handleUpload() {
      if (!file) {
        setMsg("NO FILE SELECTED");
        return;
      }
      const fd = new FormData();
      fd.append("file", file);
      setMsg("UPLOADING");
      setProgress(prevState => ({...prevState,started:true}));

      axios.post("/api/upload", fd, {
        onUploadProgress: (progressEvent) => {setProgress(prevState => ({...prevState,pc:Math.round((progressEvent.loaded * 100) / (progressEvent.total ?? 0))}))},
        headers: {
          "Custom-Header": "value",
        },
      })
      .then(response => {
        setMsg("Upload Succesful");
        console.log("File uploaded successfully", response.data);
      })
      .catch(error => {
        setMsg("Upload Failed");
        console.error("Error uploading file", error);
      });
    }
    
  return (
    <>
    <div className="app">
      <h1> Upload the file</h1>

      <input
  onChange={(e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  }}
  type="file"
/>

      <button onClick={handleUpload}>Upload  </button>

      {progress.started && <progress value={progress.pc} max="100" />}
      {msg && <span>{msg}</span>}
    </div>
    </>
    
    
   
  );
}
