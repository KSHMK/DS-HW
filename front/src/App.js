import { useEffect, useState } from 'react';

import NavBar from './Navbar';
import Search from './Search';
import Upload from './Upload';
import Result from './Result';



const App = () => {
  const [navState, setNavState] = useState('upload');
  const [curHash, setCurHash] = useState('');
  const [isStarted, setIsStarted] = useState(false);


  const navResult = () =>  {
    if(navState === 'upload'){
      return <Upload setCurHash={setCurHash} setNavState={setNavState}/>
    }
    if(navState ===  'result')
      return <Result isStarted={isStarted} setIsStarted={setIsStarted} curHash={curHash}/>
    if(navState === 'search'){
      return <Search setCurHash={setCurHash} setNavState={setNavState}/>
    }
  }

  return (
    <>
      <NavBar setCurHash={setCurHash} setNavState={setNavState}  />
      {
        navResult()
      }
    </>
  )
}

export default App;
