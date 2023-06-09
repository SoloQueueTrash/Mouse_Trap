import 'package:app/trap.dart';
import 'package:flutter/material.dart';

class AddTrapScreen extends StatefulWidget {
  @override
  _AddTrapScreenState createState() => _AddTrapScreenState();
}

class _AddTrapScreenState extends State<AddTrapScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _ipController = TextEditingController();
  final _portController = TextEditingController();

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

  TextFormField _buildIpField() {
    return TextFormField(
      controller: _ipController,
      decoration: const InputDecoration(
        labelText: 'IP Address',
        border: OutlineInputBorder(),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter an IP address';
        }
        return null;
      },
    );
  }

  TextFormField _buildPortField() {
    return TextFormField(
      controller: _portController,
      decoration: const InputDecoration(
        labelText: 'Port',
        border: OutlineInputBorder(),
      ),
      validator: (value) {
        if (value == null || value.isEmpty) {
          return 'Please enter a port';
        }
        return null;
      },
    );
  }

  ElevatedButton _buildSubmitButton(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        if (_formKey.currentState!.validate()) {
          Navigator.pop(
            context,
            Trap(
              name: _nameController.text,
              ip: _ipController.text,
              port: int.parse(_portController.text),
            ),
          );
        }
      },
      child: const Text('Add'),
    );
  }

  ElevatedButton _buildCancelButton(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        Navigator.pop(context);
      },
      child: const Text('Cancel'),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _ipController.dispose();
    _portController.dispose();
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
            const SizedBox(height: 16),
            _buildIpField(),
            const SizedBox(height: 16),
            _buildPortField(),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                _buildCancelButton(context),
                const SizedBox(width: 16),
                _buildSubmitButton(context),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
