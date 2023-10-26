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
        public List<List<string>> room_state = new();
        public List<int> vacuum_pos;
    }

    // Initializing game_objects:
    public GameObject CleanCell;
    public GameObject DirtyCell;
    public GameObject ObstacleCell;
    public GameObject ChargerCell;

    TcpClient client;
    NetworkStream stream;
    void Start()
    {
        client = new TcpClient("localhost", 12345);
        stream = client.GetStream();
        // Reading data from the stream:
        byte[] buffer = new byte[1024];
        int bytesRead = stream.Read(buffer, 0, buffer.Length);

        // Converting bytes to a .json:
        string jsonString = System.Text.Encoding.UTF8.GetString(buffer, 0, bytesRead);
        Debug.Log("Received JSON: " + jsonString);


        // Deserializing .json string into an object of the RoomState class:
        RoomState initialRoomState = JsonUtility.FromJson<RoomState>(jsonString);
        Debug.Log("Initial room state: " + (initialRoomState == null ? "null" : "not null"));
        CreateRoom(initialRoomState);
    }


    void CreateRoom(RoomState roomState)
    {
        Debug.Log("Here's the room: " + roomState);
        Debug.Log("CreateRoom function called");
        Debug.Log("Rows in room_state: " + roomState.room_state.Count);
        if (roomState.room_state.Count > 0) {
            Debug.Log("Columns in first row: " + roomState.room_state[0].Count);
        }
        Debug.Log("Entering outer loop");
        for (int i = 0; i < roomState.room_state.Count; i++)
        {
            Debug.Log("Entering inner loop for row " + i);
            for (int j = 0; j < roomState.room_state[i].Count; j++)
            {
                GameObject cellPrefab;
                Vector3 position = new Vector3(i, j, 0);

                // Creating the actual room:
                switch (roomState.room_state[i][j])
                {
                    case "Clean":
                        cellPrefab = CleanCell;
                        break;
                    case "Dirty":
                        cellPrefab = DirtyCell;
                        break;
                    case "Obstacle":
                        cellPrefab = ObstacleCell;
                        break;
                    case "Charger":
                        cellPrefab = ChargerCell;
                        break;
                    default:
                        cellPrefab = CleanCell;
                        break;
                }

                if (cellPrefab != null)
                {
                    Debug.Log("Instantiating " + roomState.room_state[i][j] + " at " + position);
                    GameObject newCell = Instantiate(cellPrefab, position, Quaternion.identity);

                    // If the cell is an obstacle, randomly choose a variant
                    if (roomState.room_state[i][j] == "Obstacle")
                    {
                        int randomIndex = UnityEngine.Random.Range(0, newCell.transform.childCount);
                        for (int k = 0; k < newCell.transform.childCount; k++)
                        {
                            newCell.transform.GetChild(k).gameObject.SetActive(k == randomIndex);
                        }

                    }
                }
            }
        }
    }

    void Update()
    {
        // if (stream.DataAvailable)
        // {
        //     // // Reading data from the stream:
        //     // byte[] buffer = new byte[1024];
        //     // int bytesRead = stream.Read(buffer, 0, buffer.Length);

        //     // // Converting bytes to a .json:
        //     // string jsonString = System.Text.Encoding.UTF8.GetString(buffer, 0, bytesRead);

        //     // // Deserializing .json string into an object of the RoomState class:
        //     // RoomState roomState = JsonUtility.FromJson<RoomState>(jsonString);
        // }
    }
    void OnDestroy()
    {
        // Close the socket connection when the game object is destroyed
        stream.Close();
        client.Close();
    }
}
