from rest_framework import serializers
from base.models import SubstrateNode, SubstrateLink, VirtualNetwork, LogicalNode, LogicalLink, Mapping

class SubstrateNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstrateNode
        fields = ('id', 'name', 'capacity', 'created_at', 'updated_at')

class SubstrateLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubstrateLink
        fields = ('id', 'name', 'source_substrate_node', 'target_substrate_node', 'bandwidth', 'created_at', 'updated_at')

class VirtualNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualNetwork
        fields = ('id', 'name', 'created_at', 'updated_at')

class LogicalNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicalNode
        fields = ('id', 'name', 'virtual_network', 'created_at', 'updated_at', 'substrate_node', 'capacity')

class LogicalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicalLink
        fields = ('id', 'name', 'source_logical_node', 'substrate_links','target_logical_node', 'bandwidth', 'virtual_network', 'created_at', 'updated_at')

class MappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapping
        fields = ('id', 'substrate_link', 'logical_link', 'created_at', 'updated_at')

# Path: api\views.py