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
            
    public void writeSocket(byte[] data)
    {
        if (!socket_ready)
            return;

        int head = data.Length + 4;
        this.socket_writer_binary.Write(head);
        this.socket_writer_binary.Write(data);
        this.socket_writer_binary.Flush();
    }

    public byte[] readSocket()
    {
        if (!socket_ready)
            return null;

        byte[] data = null;

        if (net_stream.DataAvailable)
        {
            int head = socket_reader_binary.ReadInt32();
            head -= 4;

            data = socket_reader_binary.ReadBytes(head);
            return data;
        }

        return data;
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