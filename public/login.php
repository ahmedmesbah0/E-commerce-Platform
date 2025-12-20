<?php
/**
 * Login Page
 */

require_once __DIR__ . '/../config/config.php';
require_once __DIR__ . '/../classes/Auth.php';

$auth = new Auth();

// Redirect if already logged in
if ($auth->isLoggedIn()) {
    header('Location: /user/dashboard.php');
    exit;
}

$error = '';
$redirect = $_GET['redirect'] ?? '/';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    $remember = isset($_POST['remember']);

    $result = $auth->login($email, $password, $remember);

    if ($result['success']) {
        header('Location: ' . $redirect);
        exit;
    } else {
        $error = $result['message'];
    }
}

$pageTitle = "Login";
require_once __DIR__ . '/../includes/header.php';
?>

<div class="container" style="padding: 3rem 1.5rem;">
    <div style="max-width: 450px; margin: 0 auto">
        <div style="background: white; padding: 2.5rem; border-radius: 1rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
            <h1 style="text-align: center; margin-bottom: 2rem;">Welcome Back!</h1>

            <?php if ($error): ?>
                <div class="alert alert-error">
                    <?php echo htmlspecialchars($error); ?>
                </div>
            <?php endif; ?>

            <form method="POST" action="">
                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Email Address</label>
                    <input type="email" name="email" required
                        value="<?php echo htmlspecialchars($_POST['email'] ?? ''); ?>"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="your@email.com">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Password</label>
                    <input type="password" name="password" required
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="••••••••">
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                        <input type="checkbox" name="remember" style="width: 18px; height: 18px;">
                        <span>Remember me</span>
                    </label>
                    <a href="/forgot-password.php" style="color: #6366f1;">Forgot password?</a>
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem; font-size: 1.125rem;">
                    Login
                </button>
            </form>

            <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e5e7eb;">
                <p style="color: #6b7280;">Don't have an account?</p>
                <a href="/register.php<?php echo $redirect != '/' ? '?redirect=' . urlencode($redirect) : ''; ?>"
                    class="btn btn-outline" style="margin-top: 1rem;">
                    Create Account
                </a>
            </div>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>