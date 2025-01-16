import React,{useEffect} from 'react'

const Toast = ({show,msg,setShow}) => {
  const duration=2000;

  useEffect(() => {
    const timeout = setTimeout(() => {
      setShow(false)
    }, duration);
    return () => clearTimeout(timeout);
  }, [show]);

  return (
    <div className={`toast-container ${show ? 'toast-show':'toast-hide'}`}>
      <p className='toast-msg'> 
        <span>{msg}</span> 
        <span className='cross' onClick={()=>setShow(false)}>x</span>
      </p>
    </div>
  )
}

export default Toast;