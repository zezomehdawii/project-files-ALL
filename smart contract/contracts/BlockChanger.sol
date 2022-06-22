pragma solidity ^0.5.1;

contract BlockChanger{
    enum State {ACTIVE , DOWN} //Define the device state on the network (defined by the admin)
    uint  deviceCount = 0;
    address [] signed_addresses; // all used addresses are stored here

    struct admin {
        address addr;
        string username;
        string password;
        bool isAdminLoggedIn;
        bool isAdded;
    }
    admin adminInfo;

    function pushAdminInfo (address _address, string memory _username, string memory _password) public 
    {   
        adminInfo.addr = _address;
        adminInfo.username = _username; 
        adminInfo.password = _password;
        adminInfo.isAdded = true;
        adminInfo.isAdminLoggedIn = false;
    }

    function checkIsAdded() public view returns (bool)
    {
        return adminInfo.isAdded;
    }

    // function testAdminInfo () public view returns (address, string memory, string memory, bool, bool) 
    // {
    //     return (adminInfo.addr,adminInfo.username, adminInfo.password, adminInfo.isAdminLoggedIn, adminInfo.isAdded);
    // }


    function loginUser(address _address, string memory _username, string memory _password) public   //chek for admin users
    {
        if (adminInfo.addr == _address)
        {
            if (keccak256(abi.encodePacked(adminInfo.username)) == keccak256(abi.encodePacked(_username)))
            {
                if (keccak256(abi.encodePacked(adminInfo.password)) == keccak256(abi.encodePacked(_password))) 
                {
                    adminInfo.isAdminLoggedIn = true;
                } 
                
            }
        }
    }

    function checkAdminIsLoggedIn() public view returns (bool)
    {
        return adminInfo.isAdminLoggedIn;
    }

    function logout() public
    {
        adminInfo.isAdminLoggedIn = false;
    }

    modifier onlyAdmin() 
    {
        require(msg.sender == adminInfo.addr);
        _;
    }

    struct Device_Info
    {
        string name;
        string hash_id;
        string ip;
        string mac;
        State device_state;
    }
    mapping (address => Device_Info) device;


    function add_device (address _addr, string memory _name, string memory _hash_id, string memory _ip, string memory _mac) public onlyAdmin
    {
        signed_addresses.push(_addr);
        device[_addr].name = _name;
        device[_addr].hash_id = _hash_id;
        device[_addr].ip = _ip;
        device[_addr].mac = _mac;
        device[_addr].device_state = State.ACTIVE;
        deviceCount += 1;
    }

    function getCount () public onlyAdmin view returns (uint)
    {
        return deviceCount;
    }
    
    function displayInfo(address _addr) public onlyAdmin view returns (address, string memory , string memory, string memory, string memory, State) // by address
    {
        return(_addr, device[_addr].name, device[_addr].hash_id, device[_addr].ip, device[_addr].mac, device[_addr].device_state);
    }

    function displayByName(string memory _Name ) public onlyAdmin view returns (address, string memory , string memory, string memory, string memory ,State) //by name
    {
        for (uint i = 0; i < signed_addresses.length ; i++)
        {
            if (keccak256(abi.encodePacked(_Name)) == keccak256(abi.encodePacked(device[signed_addresses[i]].name)))
            {
                return(signed_addresses[i], device[signed_addresses[i]].name, device[signed_addresses[i]].hash_id, device[signed_addresses[i]].ip, device[signed_addresses[i]].mac, device[signed_addresses[i]].device_state); 
            }
        }
        
    }

    function authFunc (string memory _hash_id) public view returns (bool)  
    {
        for (uint i = 0; i < signed_addresses.length ; i++)
        {
            if (keccak256(abi.encodePacked(_hash_id)) == keccak256(abi.encodePacked(device[signed_addresses[i]].hash_id)))
            {
                if(device[signed_addresses[i]].device_state == State.ACTIVE)
                {
                    return true;
                }
            }
        }
        return false;     
    }   


    function Activate (string memory _name) public onlyAdmin
    {
        for (uint i = 0; i < signed_addresses.length ; i++)
        {
            if (keccak256(abi.encodePacked(_name)) == keccak256(abi.encodePacked(device[signed_addresses[i]].name)))
            {
                device[signed_addresses[i]].device_state = State.ACTIVE;
            }
        }
    }

    function deActivate (string memory _name) public onlyAdmin
    {
        for (uint i = 0; i < signed_addresses.length ; i++)
        {
            if (keccak256(abi.encodePacked(_name)) == keccak256(abi.encodePacked(device[signed_addresses[i]].name)))
            {
                device[signed_addresses[i]].device_state = State.DOWN;
            }
        }
    }

}