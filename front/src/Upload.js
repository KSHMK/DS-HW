import { useState } from 'react';

import {
  Heading,
  Button,
  Progress,
  Input,
  Box,
  Text,
  Grid,
  GridItem,
} from '@chakra-ui/react'
import axios from 'axios';

const Upload = ({setCurHash, setNavState}) => {

  const [progress, setProgress] = useState(0);
  const [msg, setMsg] = useState('');
  const [selectedFile, setSelectedFile] = useState();
  const [isSelected, setIsSelected] = useState(false);
  const [isUpload, setIsUpload] = useState(false);
  

  const changeHandler = (event) => {
    if(event.target.files[0] === undefined){
      setIsSelected(false);
      return;
    }
    setSelectedFile(event.target.files[0]);
    setIsSelected(true);
  };

  async function upload(){
    if(!isSelected || isUpload)
      return;
    
    
    setIsUpload(true);
    setMsg('Uploading');
    setProgress(0);
    
    try{
      let formData = new FormData(); // formData 객체를 생성한다.

      formData.append("file", selectedFile);
      const config = {
        onUploadProgress: progressEvent => setProgress((progressEvent.loaded/progressEvent.total*100).toFixed()),
        headers: {"Content-Type": "multipart/form-data"}
      }
      const result = await axios.post("http://192.168.5.100:8080/sample",formData,config);
      console.log(result);

      setNavState('result');
      setCurHash(result.data.hash);

    } catch(err) {
      setMsg("Error");
      
    }
    setIsUpload(false);
    setProgress(0);
    
  }

  return (
    <Box 
    maxH="30em" 
    
    px={{base:20}}
    py={{base:10}}>
      <Heading py={{base:5}}>Upload File</Heading>
        <Box py={{base:5}}>
          <Input type="file" name="file" onChange={changeHandler} accept="*" />
        </Box>
        <Box py={{base:5}}>
        <Grid gap={4}>
          <GridItem colSpan={1}><Text>{msg}</Text></GridItem> 
          <GridItem colSpan={1}><Progress value={progress} size='lg'/></GridItem>
        </Grid>
        </Box>
        <Button 
        isLoading={isUpload}
        loadingText='Uploading'
        colorScheme='blue' 
        mr={3} 
        onClick={upload}>
          Start Upload
        </Button>
        
    </Box>
  )
}
export default Upload;