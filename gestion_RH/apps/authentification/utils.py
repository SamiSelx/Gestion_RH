from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

# Create class that generate token using class PasswordResetTokenGenerator (this class has method make_hash_value)
class TokenGenerator(PasswordResetTokenGenerator):
    # utilise l'algorithme sha125
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.isActive)
    
generate_token = TokenGenerator()