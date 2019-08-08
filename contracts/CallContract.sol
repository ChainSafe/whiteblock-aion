pragma solidity ^0.5.0;

contract CallContract {

    address private calleeAddress;

    function callOtherContract(uint currentDepth, uint targetDepth) public returns (bool) {
        //implicitly true
        bool success = true;
        bytes4 sig = bytes4(keccak256("callOtherContract(uint,uint)")); //Function signature
        uint nextDepth = currentDepth++;
        address calleeAddr = calleeAddress;
        if (currentDepth < targetDepth) {
            //someone please double check this :)
            uint g = gasleft();
            assembly{

                let ptr := mload(0x40)          //Find empty storage location using "free memory pointer"
			    mstore(ptr,sig)                 //Place signature at begining of empty storage
                mstore(add(ptr,0x04),nextDepth) //First uint parameter, add 4 bytes just after signature ptr start location
                mstore(add(ptr,0x24),targetDepth)         //2nd uint parameter placed right after the first parameter, add 36 bytes after the signature ptr start location
			    mstore(0x40,add(ptr,0x64))      //Reset free pointer before the function call

			    let returnValue := call(
                                    g,              //gas left
				                    calleeAddr,  //To address
				                    0,              //value, we pass in none
				                    ptr,            //inputs start at location ptr
				                    0x44,           //size of inputs total, 68 bytes (4 (sig) + 32 (uint) + 32 (uint))
				                    ptr,            //overwrite input with output
				                    0x20)           //output 32 bytes long, (fun fact: even though a bool is a uint8 it's stored as uint256)

                //jump to throw destination if this throws ie returnValue == 0
			    jumpi(0x02,iszero(returnValue))
			    //set success to true
			    success := mload(ptr)
		    }

        }

        return success;
    }

    function setOtherCallee(address callee) public {
        calleeAddress = callee;
    }

}