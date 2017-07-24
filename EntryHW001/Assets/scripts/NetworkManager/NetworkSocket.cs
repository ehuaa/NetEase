using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.Net.Sockets;


public class NetworkSocket : MonoBehaviour {

    public String host = "localhost";
    public Int32 port = 5001;

    internal Boolean socket_ready = false;
    internal String input_buffer = "";
    TcpClient tcp_socket;
    NetworkStream net_stream;

    StreamWriter socket_writer;
    StreamReader socket_reader;

    BinaryWriter socket_writer_binary;
    BinaryReader socket_reader_binary;
    

    public static NetworkSocket instance = null;

    void Awake()
    {
        if (instance!= null)
        {
            GameObject.Destroy(this.gameObject);
            return;
        }

        instance = this;

        //Keep the Network Manager alive when change scene.
        DontDestroyOnLoad(transform.gameObject);

        setupSocket();
    }
    

    void Update()
    {
        string received_data = readSocket();
        
        if (received_data != "")
        {
        	// Do something with the received data,
        	// print it in the log for now
            Debug.Log(received_data);
        }
    }


    void OnApplicationQuit()
    {
        closeSocket();
    }

    public void setupSocket()
    {
        try
        {
            tcp_socket = new TcpClient(host, port);

            net_stream = tcp_socket.GetStream();
            
            socket_writer_binary = new BinaryWriter(net_stream);
            socket_reader_binary = new BinaryReader(net_stream);            

            socket_ready = true;
        }
        catch (Exception e)
        {
        	// Something went wrong
            Debug.Log("Socket error: " + e);
        }
    }

    public BinaryWriter GetWriteSocket()
    {
        if (!socket_ready)
        {
            return null;
        }

        return this.socket_writer_binary;
    }

    public void writeSocket(string line)
    {
        if (!socket_ready)
            return;

        byte[] data = System.Text.Encoding.Default.GetBytes(line);

        int size = data.Length;
        
        size += 8;

        socket_writer_binary.Write(size);
        socket_writer_binary.Write(data.Length);        
        socket_writer_binary.Write(data);
        socket_writer_binary.Flush();
    }

    public String readSocket()
    {
        if (!socket_ready)
            return "";
        
        if (net_stream.DataAvailable)
        {
            int code = socket_reader_binary.ReadInt32();
            byte[] buf = socket_reader_binary.ReadBytes(code - 4);
            string msg = System.Text.Encoding.Default.GetString(buf);

            Debug.Log("server to client:" + msg);
        }
           

        return "";
    }

    public void closeSocket()
    {
        if (!socket_ready)
            return;

        socket_writer_binary.Close();
        socket_reader_binary.Close();
        tcp_socket.Close();
        socket_ready = false;
    }

}