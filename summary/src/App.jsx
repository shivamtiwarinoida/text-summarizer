import { useState } from 'react'
import './App.css'
import Toast from './components/Toast';
import axios from 'axios';
import LoadingSpinner from "./components/LoadingSpinner";

function App() {
  const [val,setVal]=useState("");
  const [out,setOut]=useState("");
  const [show,setShow]=useState(false);
  const [msg,setMsg]=useState("Sample Message");
  const [loading,setloading]=useState(false);

  const handleClick=async()=>{
    if(val.length<80){  
      callToast("Please enter an Article");
      return 
    }
    
    setOut("");
    setloading(true);
    try{
      const res=await axios.post("http://127.0.0.1:5000/summary",{
        "article":val,
      },{
        headers: {
          'Content-Type': 'application/json', // Adjust this depending on what the server expects
        }
      })
      if(res.data.response!=null){
        setOut(res.data.response);
        setloading(false);
      }  
    }
    catch(err){
      console.log(err);
      callToast("Something Went Wrong");
    }
    setVal("");
  }

  const callToast=(msg="Sample MSg")=>{
    setShow(true);
    setMsg(msg);
  }

  return (
    <div className='main scrollable-container'>
      <Toast show={show} msg={msg} setShow={setShow}/>
      <h2 className='head'>
        <span>Text Summary</span>
        <span className='info' onClick={()=>callToast("It is a Text Summarizer.")}>info</span>
        </h2>
      <div className='inp-container'>
        <textarea type='text' value={val} 
        onChange={(e)=>setVal(e.target.value)}
        rows={12} className='inputs' placeholder='Enter the text'/>
        <button onClick={handleClick} className='btn'>Submit</button>
        {
          loading && <LoadingSpinner/>
        }
        {
          out!=="" && 
          <div className='w-9'>
            <h5 className='out-head'>Summary</h5>  
            <p className='out-para'>{out}</p>
          </div>
        }
      </div>
      <div className='footer'>Made by Shiv</div>
    </div>
  )
}

export default App
