import React,{useState, useRef} from 'react'
import {RiCloseCircleFill} from 'react-icons/ri'
import {IoEnterOutline} from 'react-icons/io5'
import {Link} from 'react-router-dom'
import {registration} from '../actions/user'
const Registration = () => {
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('') 
    const [inp1, setInp1] = useState('inp1')
    const [passinp1, setPassinp1] = useState('passinp1')
    const [nameinp1, setNameinp1] = useState('nameinp1')
    
    
    const nameref = useRef()
    const eref = useRef()
    const passref = useRef()
    // validation
    const validStatus = {}
    if(email && !/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email)){
      console.log('no')
      validStatus.status = false}else{
        validStatus.status = true
      }
    if(password && password.length<6){
      validStatus.passErr = false
    }else{
      validStatus.passErr =true
    }
    if(password.length >0 && email.length>0 && name.length>0 && validStatus.passErr && validStatus.status){
      validStatus.disable = true
    }
    
  // Email
    const emailFocus= () => {
      setInp1('inp2')
      setEmail('')
      eref.current.focus()
    }
    const emailBlur = () => {
      email === '' && setInp1('inp1')
    }
//password
    const passFocus= () => {
      setPassinp1('passinp2')
      setPassword('')
      passref.current.focus()
    }
    const passBlur = () => {
      password === '' && setPassinp1('passinp1')
    }
// name
    const nameFocus= () => {
      setNameinp1('nameinp2')
      setName('')
      nameref.current.focus()
    }
    const nameBlur = () => {
      name === '' && setNameinp1('nameinp1')
    }

    const formHandler = (e) => {
      e.preventDefault()

     registration(name, email, password)
    }

    return (
          <div style={{display:'flex', justifyContent:'center', marginTop:'5%'}}>

            <form onSubmit={formHandler} >
            <div>
            <div className={nameinp1}>Name</div>
            <input ref={nameref} type='text'style={{width:'330px'}} value={name} onFocus={nameFocus} 
            onChange={e=>setName(e.target.value)} onBlur={nameBlur} required/>   
            { name && <RiCloseCircleFill onClick={nameFocus} style={{color:'orange', position:'absolute',marginTop:'6px', marginLeft:'-23px'}}/>}
            </div>     

            <div style={{marginTop:'30px'}} >
            <div className={inp1}>Email</div>
            <input type='email' ref={eref} value={email} style={{width:'330px'}} 
             onFocus={emailFocus} onChange={e=>setEmail(e.target.value)} onBlur={emailBlur} required/>   
            { email && <RiCloseCircleFill onClick={emailFocus} style={{color:'orange', position:'absolute',marginTop:'6px', marginLeft:'-23px'}}/>}
            {validStatus && !validStatus.status && <div style={{fontSize:'12px', color:'red'}}>Enter a valid Email address</div>}
            </div>      

            <div style={{marginTop:'30px'}} >
            <div className={passinp1}>Password</div>
            <input type='password' autoComplete='on'
             value={password} ref={passref} style={{width:'330px'}} onFocus={passFocus} 
            onChange={e=>setPassword(e.target.value)} onBlur={passBlur} required/>   
            { password && <RiCloseCircleFill onClick={passFocus} style={{color:'orange', position:'absolute',marginTop:'6px', marginLeft:'-23px'}}/>}
            {validStatus &&  !validStatus.passErr && <div style={{fontSize:'12px', color:'red'}}>Passwords must be at least 6 characters </div>}
            </div>     

            <div style={{marginTop:'40px', textAlign:'center'}} >
            <button hidden={!validStatus.disable} className='regbtn' 
            // disabled={!validStatus.disable}
             >Register now &nbsp; &gt;&gt;</button> 
            </div>
              <div style={{marginTop:'30px', textAlign:'center'}}>
                <span style={{color:'green', fontSize:'14px', marginRight:'9px'}} >Already registered?</span>
                <Link style={{textDecoration:'none', color:'orange'}} to='/login'>Login <IoEnterOutline style={{fontSize:'22px', marginBottom:'3px'}}/></Link>
              </div>
              </form> 

          </div>
    )
}

export default Registration
