

import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Heading,
} from '@chakra-ui/react'
import axios from 'axios';

import { useState, useEffect} from 'react';


export const Result = ({isStarted, setIsStarted, curHash}) => {
  
  const [list, setList] = useState([]);
  const [time, setTime] = useState('');
  let intv;

  function viewList() {
    if(curHash === '')
      return;
    axios.get("http://192.168.5.100:8080/result/"+curHash)
    .then((res) => {console.log(res);setList(res.data.result); setTime(res.data.time)})
    .catch((err) => console.log(err));
    
  }

  useEffect(() => {
    viewList();
    console.log("HI");
    intv = setInterval(viewList, 5000)
    return () => {
      console.log("BYE");
      clearInterval(intv);
    }
  }, [])

  

  return (
    <Box 
    maxH="30em" 
    overflowY="scroll"
    px={{base:20}}
    py={{base:10}}>
      <Heading py={{base:5}}>Result: {curHash}</Heading>
      <Heading as='h4' size='md' py={{base:5}}>Upload Time: {time}</Heading>
      <Table>
        <Thead>
          <Tr>
            <Th>Node Id</Th>
            <Th>AV Name</Th>
            <Th>Result</Th>
            <Th>Result Time</Th>
          </Tr>
        </Thead>
        <Tbody>
        {
          list.length !== 0 ? 
            list.map((value, idx) => {
              return (
                <Tr key={ idx }>
                  <Td>{ value.IP }</Td>
                  <Td>{ value.AV }</Td>
                  <Td>{ value.result.toString() }</Td>
                  <Td>{ value.result_time }</Td>
                </Tr>
              )
            })
          : <Tr><Td colSpan={4}>None</Td></Tr>
          
        }
        </Tbody>
      </Table>
    </Box>
  )
}

export default Result