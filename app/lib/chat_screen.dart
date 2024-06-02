import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';
import 'theme_toggle_button.dart';
import 'message_bubble.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  ChatScreenState createState() => ChatScreenState();
}

class ChatScreenState extends State<ChatScreen> {
  final ImagePicker _picker = ImagePicker();
  final TextEditingController _diameterController = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];
  bool _isDarkTheme = false;

  void _toggleTheme() {
    setState(() {
      _isDarkTheme = !_isDarkTheme;
    });
  }

  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await _picker.pickImage(source: source);
    if (pickedFile != null) {
      setState(() {
        _requestDiameter(File(pickedFile.path));
      });
    }
  }

  void _requestDiameter(File image) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Enter Plate Diameter'),
          content: TextField(
            controller: _diameterController,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(hintText: "Enter diameter in cm"),
          ),
          actions: <Widget>[
            ElevatedButton(
              child: const Text('OK'),
              onPressed: () {
                Navigator.of(context).pop();
                _sendMessage(image, _diameterController.text);
              },
            ),
          ],
        );
      },
    );
  }

  Future<void> _sendMessage(File image, String diameter) async {
    final request = http.MultipartRequest(
        'POST', Uri.parse('http://localhost:5000/recognize'));
    request.files.add(await http.MultipartFile.fromPath('file', image.path));
    request.fields['diameter'] = diameter;
    final response = await request.send();

    if (response.statusCode == 200) {
      final responseData = await http.Response.fromStream(response);
      final data = json.decode(responseData.body);
      setState(() {
        _messages.add({
          'sender': 'user',
          'image': image,
        });
        _messages.add({
          'sender': 'helper',
          'text': 'Detected foods:\n' +
              data['predictions']
                  .map((p) => "${p['label']} (Volume: ${p['volume']} cm³)")
                  .join('\n'),
        });
      });
    } else {
      // Handle error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${response.statusCode}')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: _isDarkTheme ? ThemeData.dark() : ThemeData.light(),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Food Calorie App'),
          actions: [
            ThemeToggleButton(
                toggleTheme: _toggleTheme, isDarkTheme: _isDarkTheme),
          ],
        ),
        body: Column(
          children: [
            Expanded(
              child: ListView.builder(
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  final message = _messages[index];
                  if (message['sender'] == 'user') {
                    return MessageBubble(
                      alignment: Alignment.centerRight,
                      color: Colors.blue,
                      textColor: Colors.white,
                      content: message['image'] != null
                          ? Image.file(message['image'],
                              width: 150, height: 150)
                          : Text('You'),
                    );
                  } else {
                    return MessageBubble(
                      alignment: Alignment.centerLeft,
                      color: Colors.grey[300]!,
                      textColor: Colors.black,
                      content: Text(message['text']),
                      leading: CircleAvatar(child: Icon(Icons.android)),
                    );
                  }
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  IconButton(
                    icon: const Icon(Icons.camera_alt),
                    onPressed: () => _pickImage(ImageSource.camera),
                  ),
                  IconButton(
                    icon: const Icon(Icons.photo),
                    onPressed: () => _pickImage(ImageSource.gallery),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
