pragma solidity ^0.5.0;

contract SimpleContractWithoutABI {
    // This will have an ABI. The closest thing to a no-ABI smart contract
    // is a contract containing only a constructor, and constructors can't
    // return value in solidity. This means that we would not be able to
    // interact with an ABIless smart contract in a meaningful way like in
    // the Aion contract we are trying to replicate.
    function main() public pure returns (bytes32) {
        return 0;
    }

}
