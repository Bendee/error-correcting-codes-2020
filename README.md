# Error Correcting Codes Coursework 2020
(2020) Error Correcting Codes submodule coursework submission for the Computational Thinking module at Durham University 

## Description
This coursework involved writing functions that would implement various [error correcting codes](https://wikipedia.org/wiki/Error_correction_code), namely [repetition](https://wikipedia.org/wiki/Repetition_code) and [Hamming](https://wikipedia.org/wiki/Hamming_code) codes.

## Questions
### 1. Helper function
  * `decimalToVector(i, l)`: Returns a vector of *l* bits representing *i*.
### 2. Functions for repetition codes
  1. `repetitionEncoder(m, n)`: Returns the element of the 1x1 vector *m* repeated *n* times.
  2. `repetitionDecoder(v)`: Returns the decoded repetition code given by the vector *v*.
### 3. Functions for Hamming codes
  1. `message(a)`: Coverts *a* into a message for Hamming code.
  2. `hammingEncoder(m)`: Encodes the message *m* using Hamming code.
  3. `hammingDecoder(v)`: Decodes the Hamming code *v* using [Syndrome decoding](https://wikipedia.org/wiki/Decoding_methods#Syndrome_decoding).
  4. `messageFromCodeword(c)`: Extracts the message sent from the codeword *c*.
  5. `dataFromMessage(m)`: Recovers the raw data from the message *m*.
