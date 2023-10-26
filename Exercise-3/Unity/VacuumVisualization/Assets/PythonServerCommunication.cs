using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System;

public class PythonServerCommunication : MonoBehaviour
{
    // Defining a class that mirrors the .json structure:
    [Serializable]
    public class RoomState
    {
        public List<List<int>> room_state;
        public List<int> vacuum_pos;
    }
    TcpClient client;
    NetworkStream stream;
    void Start()
    {
        client = new TcpClient("localhost", 12345);
        stream = client.GetStream();
    }

    void Update()
    {
        if (stream.DataAvailable)
        {
            // Reading data from the stream:
            byte[] buffer = new byte[1024];
            int bytesRead = stream.Read(buffer, 0, buffer.Length);

            // Converting bytes to a .json:
            string jsonString = System.Text.Encoding.UTF8.GetString(buffer, 0, bytesRead);

            // Deserializing .json string into an object of the RoomState class:
            RoomState roomState = JsonUtility.FromJson<RoomState>(jsonString);
        }
    }
    void OnDestroy()
    {
        // Close the socket connection when the game object is destroyed
        stream.Close();
        client.Close();
    }
}
