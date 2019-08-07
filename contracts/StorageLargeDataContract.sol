pragma solidity ^0.5.0;

contract StorageLargeDataContract {
    //constant arrays not supported in solidity
    //In aion this seems to be an array of int arrays
    int[][] objectArray;


    /**
    * Tests the cost of relatively large graph storage.
    */
    function writeToObjectArray(uint objectArraySize, uint intArraySize) public {
        objectArray = new int[][](objectArraySize);
        for (uint i = 0; i < objectArray.length; i++) {
            objectArray[i] = new int[](intArraySize);
        }
    }

}