import {React,useState} from "react";
import { BrowserRouter,Routes,Route } from "react-router-dom";
// import ReactDOM from "react-dom/client";
import { Login } from './Pages/Login'
import { Home } from './Pages/Home'

function App() {
  const [login,setLogin] = useState(false);

  const setData = (data) =>{
    setLogin(data);
  }
  console.log(login)
return (
<div>
<BrowserRouter>
<Routes>
  <Route path='/' element={<Home state={login} func={setData}/>}/>
  <Route path='/login' element={<Login state={login} func={setData} />}/>
</Routes>
</BrowserRouter>

</div>
);
}

export default App;