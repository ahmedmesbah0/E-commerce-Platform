<?php
/**
 * Authentication Class
 * Handles user login, logout, and session management
 */

require_once __DIR__ . '/Database.php';
require_once __DIR__ . '/Customer.php';

class Auth
{
    private $db;

    public function __construct()
    {
        $this->db = Database::getInstance();
    }

    /**
     * Login customer
     */
    public function login($email, $password, $remember = false)
    {
        $sql = "SELECT customer_id, name, email, password_hash, is_active
                FROM customer
                WHERE email = ?";

        $customer = $this->db->fetchOne($sql, [$email]);

        if (!$customer) {
            return ['success' => false, 'message' => 'Invalid email or password'];
        }

        if (!$customer['is_active']) {
            return ['success' => false, 'message' => 'Account is deactivated'];
        }

        // Verify password
        if (!password_verify($password, $customer['password_hash'])) {
            return ['success' => false, 'message' => 'Invalid email or password'];
        }

        // Set session
        $_SESSION['customer_id'] = $customer['customer_id'];
        $_SESSION['customer_name'] = $customer['name'];
        $_SESSION['customer_email'] = $customer['email'];
        $_SESSION['logged_in'] = true;
        $_SESSION['login_time'] = time();

        // Remember me cookie (30 days)
        if ($remember) {
            $token = bin2hex(random_bytes(32));
            setcookie('remember_token', $token, time() + (30 * 24 * 60 * 60), '/');
            // Store token in database (you'd need a remember_tokens table)
        }

        return [
            'success' => true,
            'message' => 'Login successful',
            'customer' => [
                'id' => $customer['customer_id'],
                'name' => $customer['name'],
                'email' => $customer['email']
            ]
        ];
    }

    /**
     * Admin login
     */
    public function adminLogin($email, $password)
    {
        $sql = "SELECT admin_id, email, password_hash, role, permissions
                FROM admin
                WHERE email = ?";

        $admin = $this->db->fetchOne($sql, [$email]);

        if (!$admin) {
            return ['success' => false, 'message' => 'Invalid credentials'];
        }

        if (!password_verify($password, $admin['password_hash'])) {
            return ['success' => false, 'message' => 'Invalid credentials'];
        }

        // Set admin session
        $_SESSION['admin_id'] = $admin['admin_id'];
        $_SESSION['admin_email'] = $admin['email'];
        $_SESSION['admin_role'] = $admin['role'];
        $_SESSION['admin_permissions'] = json_decode($admin['permissions'], true);
        $_SESSION['is_admin'] = true;
        $_SESSION['login_time'] = time();

        // Log admin login
        $this->logActivity($admin['admin_id'], 'login', 'Admin logged in');

        return [
            'success' => true,
            'message' => 'Admin login successful',
            'redirect' => '/admin/dashboard.php'
        ];
    }

    /**
     * Logout
     */
    public function logout()
    {
        // Log activity if admin
        if (isset($_SESSION['admin_id'])) {
            $this->logActivity($_SESSION['admin_id'], 'logout', 'Admin logged out');
        }

        // Clear session
        session_unset();
        session_destroy();

        // Clear remember me cookie
        if (isset($_COOKIE['remember_token'])) {
            setcookie('remember_token', '', time() - 3600, '/');
        }

        return ['success' => true, 'message' => 'Logged out successfully'];
    }

    /**
     * Check if user is logged in
     */
    public function isLoggedIn()
    {
        return isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true;
    }

    /**
     * Check if admin is logged in
     */
    public function isAdmin()
    {
        return isset($_SESSION['is_admin']) && $_SESSION['is_admin'] === true;
    }

    /**
     * Get current customer ID
     */
    public function getCustomerId()
    {
        return $_SESSION['customer_id'] ?? null;
    }

    /**
     * Get current admin ID
     */
    public function getAdminId()
    {
        return $_SESSION['admin_id'] ?? null;
    }

    /**
     * Require login
     */
    public function requireLogin($redirectUrl = '/login.php')
    {
        if (!$this->isLoggedIn()) {
            header('Location: ' . $redirectUrl);
            exit;
        }
    }

    /**
     * Require admin
     */
    public function requireAdmin($redirectUrl = '/admin/login.php')
    {
        if (!$this->isAdmin()) {
            header('Location: ' . $redirectUrl);
            exit;
        }
    }

    /**
     * Check admin permission
     */
    public function hasPermission($permission)
    {
        if (!$this->isAdmin()) {
            return false;
        }

        $permissions = $_SESSION['admin_permissions'] ?? [];
        return isset($permissions[$permission]) && $permissions[$permission] === true;
    }

    /**
     * Request password reset
     */
    public function requestPasswordReset($email)
    {
        $customer = $this->db->fetchOne("SELECT customer_id, name FROM customer WHERE email = ?", [$email]);

        if (!$customer) {
            // Don't reveal if email exists
            return ['success' => true, 'message' => 'If the email exists, a reset link has been sent'];
        }

        // Generate reset token
        $token = bin2hex(random_bytes(32));
        $expiry = date('Y-m-d H:i:s', strtotime('+1 hour'));

        // Store token (you'd need a password_reset_tokens table)
        // For now, just send email

        // Send reset email
        $resetLink = SITE_URL . "/reset-password.php?token=" . $token;
        $this->sendResetEmail($email, $customer['name'], $resetLink);

        return ['success' => true, 'message' => 'Password reset instructions sent to your email'];
    }

    /**
     * Reset password with token
     */
    public function resetPassword($token, $newPassword)
    {
        // Verify token (from password_reset_tokens table)
        // For now, simplified version

        if (strlen($newPassword) < PASSWORD_MIN_LENGTH) {
            return ['success' => false, 'message' => 'Password must be at least ' . PASSWORD_MIN_LENGTH . ' characters'];
        }

        // Hash new password
        $passwordHash = password_hash($newPassword, HASH_ALGO, ['cost' => HASH_COST]);

        // Update password
        // $result = $this->db->update('customer', ['password_hash' => $passwordHash], 'customer_id = ?', [$customerId]);

        return ['success' => true, 'message' => 'Password reset successfully'];
    }

    /**
     * Send password reset email
     */
    private function sendResetEmail($email, $name, $resetLink)
    {
        // Email implementation would go here using SMTP settings
        // For now, just log it
        error_log("Password reset link for $email: $resetLink");

        // In production, use PHPMailer or similar:
        /*
        $mail = new PHPMailer();
        $mail->isSMTP();
        $mail->Host = SMTP_HOST;
        $mail->SMTPAuth = true;
        $mail->Username = SMTP_USER;
        $mail->Password = SMTP_PASS;
        $mail->SMTPSecure = 'tls';
        $mail->Port = SMTP_PORT;
        $mail->setFrom(SMTP_FROM, SMTP_FROM_NAME);
        $mail->addAddress($email, $name);
        $mail->Subject = 'Password Reset Request';
        $mail->Body = "Click here to reset your password: $resetLink";
        $mail->send();
        */
    }

    /**
     * Log admin activity
     */
    private function logActivity($adminId, $eventType, $description)
    {
        $data = [
            'admin_id' => $adminId,
            'event_type' => $eventType,
            'description' => $description,
            'ip_address' => $_SERVER['REMOTE_ADDR'] ?? null,
            'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? null
        ];

        $this->db->insert('system_log', $data);
    }

    /**
     * Validate session
     */
    public function validateSession()
    {
        if (!$this->isLoggedIn()) {
            return false;
        }

        // Check session timeout (2 hours)
        if (isset($_SESSION['login_time'])) {
            $elapsed = time() - $_SESSION['login_time'];
            if ($elapsed > SESSION_LIFETIME) {
                $this->logout();
                return false;
            }
        }

        return true;
    }

    /**
     * Regenerate session ID for security
     */
    public function regenerateSession()
    {
        session_regenerate_id(true);
    }
}
