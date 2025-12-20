</main>

<footer>
    <div class="container">
        <div class="footer-content">
            <div class="footer-section">
                <h4><?php echo SITE_NAME; ?></h4>
                <p>Your one-stop shop for quality products at great prices.</p>
                <p style="margin-top: 1rem;">📧 <?php echo SITE_EMAIL; ?></p>
            </div>

            <div class="footer-section">
                <h4>Quick Links</h4>
                <ul class="footer-links">
                    <li><a href="/about.php">About Us</a></li>
                    <li><a href="/contact.php">Contact</a></li>
                    <li><a href="/shipping.php">Shipping Info</a></li>
                    <li><a href="/returns.php">Returns</a></li>
                </ul>
            </div>

            <div class="footer-section">
                <h4>Customer Service</h4>
                <ul class="footer-links">
                    <li><a href="/faq.php">FAQ</a></li>
                    <li><a href="/support.php">Support</a></li>
                    <li><a href="/track-order.php">Track Order</a></li>
                    <li><a href="/privacy.php">Privacy Policy</a></li>
                </ul>
            </div>

            <div class="footer-section">
                <h4>My Account</h4>
                <ul class="footer-links">
                    <?php if ($isLoggedIn): ?>
                        <li><a href="/user/dashboard.php">Dashboard</a></li>
                        <li><a href="/user/orders.php">My Orders</a></li>
                        <li><a href="/user/wishlist.php">Wishlist</a></li>
                        <li><a href="/logout.php">Logout</a></li>
                    <?php else: ?>
                        <li><a href="/login.php">Login</a></li>
                        <li><a href="/register.php">Register</a></li>
                    <?php endif; ?>
                </ul>
            </div>
        </div>

        <div class="footer-bottom">
            <p>&copy; <?php echo date('Y'); ?> <?php echo SITE_NAME; ?>. All rights reserved.</p>
        </div>
    </div>
</footer>

<script src="/assets/js/main.js"></script>
</body>

</html>