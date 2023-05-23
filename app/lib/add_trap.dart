import 'package:flutter/material.dart';

class AddTrapScreen extends StatefulWidget {
  @override
  _AddTrapScreenState createState() => _AddTrapScreenState();
}

class _AddTrapScreenState extends State<AddTrapScreen> {
  final _formKey = GlobalKey<FormState>();

  @override
  void dispose() {
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
          ],
        ),
      ),
    );
  }
}
