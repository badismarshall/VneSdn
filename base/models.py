from django.db import models

# Create your models here.

    
class VirtualNetwork(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
class SubstrateNode(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class LogicalNode(models.Model):
    name = models.CharField(max_length=255)
    virtual_network = models.ForeignKey('VirtualNetwork', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    substrate_node = models.ForeignKey(SubstrateNode, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(default=1)

    def __str__(self):
        return self.name



class SubstrateLink(models.Model):
    name = models.CharField(max_length=255)
    source_substrate_node = models.ForeignKey('SubstrateNode', related_name='source_links', on_delete=models.CASCADE)
    target_substrate_node = models.ForeignKey('SubstrateNode', related_name='target_links', on_delete=models.CASCADE)
    bandwidth = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LogicalLink(models.Model):
    name = models.CharField(max_length=255)
    source_logical_node = models.ForeignKey('LogicalNode', related_name='source_links', on_delete=models.CASCADE)
    target_logical_node = models.ForeignKey('LogicalNode', related_name='target_links', on_delete=models.CASCADE)
    bandwidth = models.IntegerField()
    # substrate_links = models.ManyToManyField('SubstrateLink')
    substrate_links = models.ManyToManyField('SubstrateLink', through='Mapping')
    virtual_network = models.ForeignKey('VirtualNetwork', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Mapping(models.Model):
    substrate_link = models.ForeignKey('SubstrateLink', on_delete=models.CASCADE)
    logical_link = models.ForeignKey('LogicalLink', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.substrate_link.name} - {self.logical_link.name}"
    