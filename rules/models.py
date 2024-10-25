from django.db import models

class Node(models.Model):
    NODE_TYPE_CHOICES = [
        ('operator', 'Operator'),
        ('operand', 'Operand'),
    ]

    OPERATOR_TYPE_CHOICES = [
        ('AND', 'AND'),
        ('OR', 'OR'),
    ]

    type = models.CharField(max_length=10, choices=NODE_TYPE_CHOICES)
    operator = models.CharField(max_length=3, choices=OPERATOR_TYPE_CHOICES, null=True, blank=True)
    left = models.ForeignKey('self', related_name='left_node', on_delete=models.CASCADE, null=True, blank=True)
    right = models.ForeignKey('self', related_name='right_node', on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)  # For operand values like "age > 30"

    def __str__(self):
        # Display 'Operator: AND' or 'Operand: age > 30'
        return f'{self.type}: {self.operator if self.operator else self.value}'
