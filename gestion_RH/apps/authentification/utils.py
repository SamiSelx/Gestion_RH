from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create class that generate token using class PasswordResetTokenGenerator (this class has method make_hash_value)
class TokenGenerator(PasswordResetTokenGenerator):
    # utilise l'algorithme sha125
    def _make_hash_value(self, user, timestamp):
        # add user.isActivate to unvalid the token after change the status, timestamp for to ensures that the token changes over the time
        return str(user.pk) + str(timestamp) + str(user.isActive)
    
generate_token = TokenGenerator()