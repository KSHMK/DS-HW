import {
  Box,
  Heading,
  Container,
  Button,
  Stack,
  Input,
} from '@chakra-ui/react';
import { useState } from 'react';

const Search = ({setCurHash, setNavState}) => {
  const [hash, setHash] = useState('');

  const search = () => {
    setNavState('result');
    setCurHash(hash);
  }

  return (
    <>
      <Container maxW={'3xl'}>
        <Stack
          as={Box}
          textAlign={'center'}
          spacing={{ base: 8, md: 14 }}
          py={{ base: 20, md: 36 }}
          >
          
          <Heading>Search</Heading>
          <Input placeholder='Hash' onChange={(e) => setHash(e.target.value)} value={hash} />  
          <Button
            onClick={() => search()}
            alignSelf={'center'}
            rounded={'full'}
            colorScheme={'cyan'}
            px={6}>
            Search
          </Button>
        </Stack>
      </Container>
    </>
  );
}


export default Search