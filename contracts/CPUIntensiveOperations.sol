pragma solidity ^0.5.0;
import "github.com/OpenZeppelin/openzeppelin-contracts/contracts/math/SafeMath.sol";

contract CPUIntensiveOperations {

    using SafeMath for uint;

    //Integer square root approximation utilizing Babylonian Method and OpenZeppelin's SafeMath
    //Solidity doesn't support fixed or floating points so this is a rough approximation that
    //converges decently but is wildly inaccurate for finding the square root of small numbers

    //Note that in solidity, division rounds down
    function babylonianSqrt(uint num) public returns (uint result) {
        uint a = (num.add(1)).div(2);
        result = num;
        while (a < num) {
            result = a;
            a = ((num.div(a)).add(a)).div(2);
        }

        return result;
    }

    //Integer square root
    function sqrt(uint count, uint num) public {
        for (uint i = 0 ; i < count; i++) {
            babylonianSqrt(num);
        }
    }

    //longs are just uint64's don't need safe math here
    function fibonacciLong(uint64 index) public returns (uint64 number) {
        uint64 number = 0;
        uint64 next = 1;
        for (uint i = 0; i < index; i++) {
            uint64 previous = number;
            number = next;
            next = previous + number;
        }

        return number;
    }

    //I did not feel confident in my ability to roll my own working and tested BigInt library for solidity
    //with the time I had for this. We utilize uint256 which will overflow far before Java's BigInt which 
    //goes up to 2^int.MAX_VALUE bits.
    function fibonacciBigInteger(uint index) public returns (bytes32 number) {
        uint number = 0;
        uint next = 1;
        for (uint i = 0; i < index; i++) {
            uint previous = number;
            number = next;
            next = previous.add(number);
        }

        return bytes32(number)
    }


}
