<?php
/**
 * User Profile Page
 */

$pageTitle = "My Profile";
require_once __DIR__ . '/../../includes/header.php';
require_once __DIR__ . '/../../classes/Customer.php';

// Require login
$auth->requireLogin('/login.php');

$customer = new Customer();
$customerId = $auth->getCustomerId();

$error = '';
$success = '';

// Handle profile update
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['update_profile'])) {
        $data = [
            'name' => $_POST['name'] ?? '',
            'email' => $_POST['email'] ?? '',
            'phone' => $_POST['phone'] ?? '',
            'address' => $_POST['address'] ?? ''
        ];

        $result = $customer->update($customerId, $data);
        if ($result) {
            $_SESSION['customer_name'] = $data['name'];
            $success = 'Profile updated successfully!';
        } else {
            $error = 'Failed to update profile';
        }
    }

    // Handle password change
    if (isset($_POST['change_password'])) {
        $oldPassword = $_POST['old_password'] ?? '';
        $newPassword = $_POST['new_password'] ?? '';
        $confirmPassword = $_POST['confirm_password'] ?? '';

        if ($newPassword !== $confirmPassword) {
            $error = 'New passwords do not match';
        } elseif (strlen($newPassword) < PASSWORD_MIN_LENGTH) {
            $error = 'Password must be at least ' . PASSWORD_MIN_LENGTH . ' characters';
        } else {
            $result = $customer->updatePassword($customerId, $oldPassword, $newPassword);
            if ($result['success']) {
                $success = 'Password changed successfully!';
            } else {
                $error = $result['message'];
            }
        }
    }
}

// Get customer data
$customerData = $customer->getById($customerId);
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <h1 style="margin-bottom: 2rem;">My Profile</h1>

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

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
        <!-- Profile Information -->
        <div style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 1.5rem;">Profile Information</h3>

            <form method="POST" action="">
                <input type="hidden" name="update_profile" value="1">

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Full Name</label>
                    <input type="text" name="name" required
                        value="<?php echo htmlspecialchars($customerData['name']); ?>"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Email Address</label>
                    <input type="email" name="email" required
                        value="<?php echo htmlspecialchars($customerData['email']); ?>"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Phone Number</label>
                    <input type="tel" name="phone" value="<?php echo htmlspecialchars($customerData['phone'] ?? ''); ?>"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Address</label>
                    <textarea name="address" rows="4"
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"><?php echo htmlspecialchars($customerData['address'] ?? ''); ?></textarea>
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%;">
                    Update Profile
                </button>
            </form>
        </div>

        <!-- Change Password -->
        <div style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 1.5rem;">Change Password</h3>

            <form method="POST" action="">
                <input type="hidden" name="change_password" value="1">

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Current Password</label>
                    <input type="password" name="old_password" required
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="••••••••">
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">New Password</label>
                    <input type="password" name="new_password" required
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="••••••••">
                    <p style="font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;">
                        Minimum <?php echo PASSWORD_MIN_LENGTH; ?> characters
                    </p>
                </div>

                <div style="margin-bottom: 1.5rem;">
                    <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Confirm New Password</label>
                    <input type="password" name="confirm_password" required
                        style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                        placeholder="••••••••">
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%;">
                    Change Password
                </button>
            </form>

            <!-- Account Info -->
            <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e5e7eb;">
                <h4 style="margin-bottom: 1rem;">Account Information</h4>
                <div style="display: grid; gap: 0.5rem; color: #6b7280; font-size: 0.875rem;">
                    <div>
                        <strong>Member Since:</strong>
                        <?php echo date('M d, Y', strtotime($customerData['date_created'])); ?>
                    </div>
                    <div>
                        <strong>Account Status:</strong>
                        <span style="color: #10b981; font-weight: 600;">
                            <?php echo $customerData['is_active'] ? 'Active' : 'Inactive'; ?>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/../../includes/footer.php'; ?>