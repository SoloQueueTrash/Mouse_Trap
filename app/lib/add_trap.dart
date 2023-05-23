import 'package:flutter/material.dart';

class AddTrapScreen extends StatefulWidget {
  @override
  _AddTrapScreenState createState() => _AddTrapScreenState();
}

class _AddTrapScreenState extends State<AddTrapScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();

  TextFormField _buildNameField() {
    return TextFormField(
      controller: _nameController,
      decoration: const InputDecoration(
        labelText: 'Name',
        border: OutlineInputBorder(),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter a name';
        }
        return null;
      },
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Add Trap')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            _buildNameField(),
          ],
        ),
      ),
    );
  }
}
