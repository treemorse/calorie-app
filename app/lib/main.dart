import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:convert';

void main() {
  runApp(const FoodCalorieApp());
}

class FoodCalorieApp extends StatelessWidget {
  const FoodCalorieApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Food Calorie App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  ChatScreenState createState() => ChatScreenState();
}

class ChatScreenState extends State<ChatScreen> {
  final ImagePicker _picker = ImagePicker();
  File? _image;
  List<dynamic>? _predictions;
  Map<String, dynamic>? _volumes;

  Future<void> _pickImage(ImageSource source) async {
    final pickedFile = await _picker.pickImage(source: source);
    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
        _sendImage(_image!);
      }
    });
  }

  Future<void> _sendImage(File image) async {
    final request = http.MultipartRequest(
        'POST', Uri.parse('http://localhost:5000/recognize'));
    request.files.add(await http.MultipartFile.fromPath('file', image.path));
    final response = await request.send();

    if (response.statusCode == 200) {
      final responseData = await http.Response.fromStream(response);
      final data = json.decode(responseData.body);
      setState(() {
        _predictions = data['predictions'];
        _volumes = data['volumes'];
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
    return Scaffold(
      appBar: AppBar(
        title: const Text('Food Calorie App'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView(
              children: [
                if (_image != null) Image.file(_image!),
                if (_predictions != null)
                  ..._predictions!.map((p) => ListTile(
                        title: Text("${p['label']}"),
                        subtitle: Text("${_volumes![p['label']]} grams"),
                      )),
              ],
            ),
          ),
          Row(
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
        ],
      ),
    );
  }
}
