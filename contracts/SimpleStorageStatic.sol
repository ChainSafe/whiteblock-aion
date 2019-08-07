pragma solidity ^0.5.0;

contract SimpleStorageStatic {
    int private constant myInt = 703;
    string private constant myString = "Benchmark Testing";
    //solidity doesn't support constant arrays
    int[6] private myInt1DArray = [0,1,2,3,4,5];
    //solidity doesn't support constant maps   
    mapping (int => string) private myMap;

    constructor() public {
        myMap[0] = "zero";
        myMap[1] = "one";
        myMap[2] = "two";
        myMap[3] = "three";
        myMap[4] = "four";
    }

    // Writes KV pairs straight to account storage in solidity but padding the value
    // bytes to len 32 as well so we can pull it cleanly with mload when getting storage
    function putStorage(string memory key, string memory value) public {
        bytes32 paddedKey = convertToFittingKey(key);
        bytes32 paddedValue = convertToFittingKey(value);
        assembly {
            sstore(paddedKey, paddedValue)
        }
    }

    function getStorage(string memory key) public pure returns (bytes32 v) {
        bytes32 paddedKey = convertToFittingKey(key);
        assembly {
            let v := mload(paddedKey)
        }

        return v;
    }

    function getMyString() public pure returns (string memory) {
        return myString;
    }

    function getMyInt() public pure returns (int) {
        return myInt;
    }

    function getMyInt1DArray() public view returns (int[6] memory) {
        return myInt1DArray;
    }

    function putMap(int key, string memory value) public {
        myMap[key] = value;
    }

    function getMap(int key) public view returns (string memory) {
        return myMap[key];
    }

    //lossy string to bytes32 conversion
    function convertToFittingKey(string memory s) public pure returns (bytes32 result) {
        assembly {
            let result := mload(add(s, 32))
        }
        return result;
    }




}