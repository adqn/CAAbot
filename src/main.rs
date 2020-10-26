use std::io::prelude::*;
use std::io::{Read, Write};
use std::io::BufReader;
use std::net::{TcpStream};
use std::str::from_utf8;

use std::sync::mpsc::{Sender, Receiver};
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

use regex::Regex;

// Currently running threads
struct Threads {

}

// Currently loaded/unloaded modules
struct Modules {

}

// Stores and handles bot environment
struct Bot {
    running: bool,
    channels: Vec<String>,
    current_message: Option<String>,
    //modules: Some(Vec<M>),
    //threads: Some(Vec<T>),
}

impl Bot {
    fn new(channels: Vec<String>) -> Bot {
        Bot{
            running: true,
            channels,
            current_message: None,
            //modules: vec![None],
            //threads: None,
        }
    }
}


fn connect(server: String, port: Option<String>) -> Option<TcpStream> {
    let mut conn: TcpStream;
    let mut host = server.to_owned();

    let mut port = match port {
        Some(port) => port,
        None => String::from("6667"),
    };
   
    host.push_str(":");
    host.push_str(&port);

    println!("Connecting to host...");

    match TcpStream::connect(host) {
        Ok(mut stream) => {
            Some(stream)
        },
        Err(e) => {
            println!("error: {}", e);
            None
        }
    }
}

fn get_resp(mut stream: &TcpStream) -> Option<String> {
    let mut data = [0u8; 2048];

    match stream.read(&mut data) {
        Ok(_) => {
            let text = from_utf8(&data).unwrap();
            Some(String::from(text))
        },
        Err(e) => {
            println!("error: {}", e);
            None
        }
    }
}

fn send(mut stream: &TcpStream, msg: &str) {
    let mut msg = String::from(msg).to_owned();
    msg.push_str("\n");
    stream.write(msg.as_bytes()).unwrap();
}

fn server_thread(stream: &TcpStream, sender: &Sender<String>) {
    let ping_re = Regex::new(r"PING").unwrap();
    let pong_re = Regex::new(r"PONG \d+").unwrap();
    let response: String;
 
    response = match get_resp(&stream){
        None => String::from("Couldn't receive message from server"),
        Some(resp) => {
            println!("{}", resp);
           
            // Reply to server ping
            if ping_re.is_match(&resp[..]) {
                send(&stream, "PONG :pingis\n");
            } 

            // Reply to initial pong request> to complete connection
            if pong_re.is_match(&resp[..]) {
                for cap in pong_re.captures_iter(&resp[..]) {
                    send(&stream, &cap[0]);
                }
            }

            resp
        }
    };
   
    sender.send(response).unwrap();
}

fn main() {
    let (tx, rx): (Sender<String>, Receiver<String>) = mpsc::channel();

    let mut bot = Bot::new(vec![String::from("#afafaf")]);
    let ident = "USER owo test tet test :test";    
    let nick = "NICK CAA_rust_test";

    let hostip = String::from("irc.rizon.net");
    let port = Some(String::from("6667"));

    match connect(hostip, port) {
       Some(s) => {
            println!("Successfully connected");
 
            // Send our identity and set nickname
            send(&s, ident);
            send(&s, nick);           
           
            // Spawn thread for persistent server connection
            let sthread = thread::spawn(move || {
                if bot.running == true {
                    loop {
                        server_thread(&s, &tx);
                        bot.current_message = Some(rx.recv().unwrap());
                        //println!("from tx: {}", bot.current_message.unwrap());
                    }
                }
            });
            // Put thread for receiving all messages here??

            sthread.join();
       },
       None => println!("Could't connect to host"),
    }
}
