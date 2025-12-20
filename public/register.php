<?php
/**
 * Registration Page
 */

require_once __DIR__ . '/../config/config.php';
require_once __DIR__ . '/../classes/Auth.php';
require_once __DIR__ . '/../classes/Customer.php';

$auth = new Auth();
$customer = new Customer();

// Redirect if already logged in
if ($auth->isLoggedIn()) {
    header('Location: /user/dashboard.php');
    exit;
}

$error = '';
$success = '';
$redirect = $_GET['redirect'] ?? '/';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['name'] ?? '';
    $email = $_POST['email'] ?? '';
    $phone = $_POST['phone'] ?? '';
    $address = $_POST['address'] ?? '';
    $password = $_POST['password'] ?? '';
    $confirmPassword = $_POST['confirm_password'] ?? '';

    // Validation
    if (strlen($password) < PASSWORD_MIN_LENGTH) {
        $error = 'Password must be at least ' . PASSWORD_MIN_LENGTH . ' characters';
    } elseif ($password !== $confirmPassword) {
        $error = 'Passwords do not match';
    } else {
        $result = $customer->create([
            'name' => $name,
            'email' => $email,
            'phone' => $phone,
            'address' => $address,
            'password' => $password
        ]);

        if ($result['success']) {
            // Auto-login after registration
            $auth->login($email, $password);
            header('Location: ' . $redirect);
            exit;
        } else {
            $error = $result['message'];
        }
    }
}

$pageTitle = "Register";
require_once __DIR__ . '/../includes/header.php';
?>

<div class="container" style="padding: 3rem 1.5rem;">
    <div style="max-width: 550px; margin: 0 auto;">
        <div style="background: white; padding: 2.5rem; border-radius: 1rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
            <h1 style="text-align: center; margin-bottom: 2rem;">Create Account</h1>

            <?php if ($error): ?>
                <div class="alert alert-error">
                    <?php echo htmlspecialchars($error); ?>
                </div>
            <?php endif; ?>

            <?php if ($success): ?>
                <div class="alert alert-success">
                    <?php echo htmlspecialchars($success); ?>
                </div>
            <?php endif; ?>

            <form method="POST" action="">
                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Full Name *</label>
                    <input type="text" name="name" required
                        value="<?php echo htmlspecialchars($_POST['name'] ?? ''); ?>"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="John Doe">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Email Address *</label>
                    <input type="email" name="email" required
                        value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="your@email.com">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Phone Number</label>
                    <input type="tel" name="phone" value="<?php echo htmlspecialchars($_POST['phone'] ?? ''); ?>"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="(123) 456-7890">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Address</label>
                    <textarea name="address" rows="3"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="123 Main St, City, State, ZIP"><?php echo htmlspecialchars($_POST['address'] ?? ''); ?></textarea>
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Password *</label>
                    <input type="password" name="password" required
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="••••••••">
                    <p style="font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;">
                        Minimum <?php echo PASSWORD_MIN_LENGTH; ?> characters
                    </p>
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Confirm Password *</label>
                    <input type="password" name="confirm_password" required
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="••••••••">
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem; font-size: 1.125rem;">
                    Create Account
                </button>
            </form>

            <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280;">Already have an account?</p>
                <a href="/login.php<?php echo $redirect != '/' ? '?redirect=' . urlencode($redirect) : ''; ?>"
                    class="btn btn-outline" style="margin-top: 1rem;">
                    Login
                </a>
            </div>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>