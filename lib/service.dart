import 'package:bsi_dart/bsi_dart.dart';

class VirtualHardwareService extends Service {
  String get id
  
  @override
  ServiceReference get reference =>
      Services.Hardwares.child('virtual-$hashCode');
}
