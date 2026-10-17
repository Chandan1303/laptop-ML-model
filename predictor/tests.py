# Project Title: LaptopPilot
# Subject: Software Testing and Quality Assurance
# Team Members:
# USN1: 4NI23IS252
# Name1: Dayanand Shivananda Sagar
# USN2: 4NI23IS253
# Name2: Chandan Shridhar Hegde
# USN3: 4NI24IS408
# Name3: Harsha S
# USN4: 4NI24IS412
# Name4: Mohammad Masood Hassan HA
# Date of code writing: 14-09-2026 to 25-09-2026

import numbers
import os

from django.test import TestCase
from django.urls import reverse

from predictor import views


class LaptopProjectQATestCase(TestCase):
    """QA-focused tests covering the main app flows and validation rules."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand_post = {
            'price': '52000',
            'rating': '4.5',
            'screen_size': '15.6',
            'storage_gb': '512',
            'ram_gb': '16',
            'cpu': 'Intel Core i5',
            'os': 'Windows 11',
            'graphics': 'NVIDIA GeForce RTX 4060',
        }
        cls.price_brand = views.BRAND_CHOICES[0]
        cls.price_rules = views.get_brand_feature_rules(cls.price_brand)
        cls.price_cpu = next(
            value for value in sorted(views.p_le_cpu.classes_.tolist())
            if any(token.lower() in str(value).lower() for token in cls.price_rules['cpu_tokens'])
        )
        cls.price_os = next(
            value for value in sorted(views.p_le_os.classes_.tolist())
            if any(token.lower() in str(value).lower() for token in cls.price_rules['os_tokens'])
        )
        cls.price_graphics = next(
            value for value in sorted(views.p_le_gfx.classes_.tolist())
            if any(token.lower() in str(value).lower() for token in cls.price_rules['graphics_tokens'])
        )
        cls.price_post = {
            'brand': cls.price_brand,
            'rating': '4.6',
            'screen_size': '14.0',
            'storage_gb': '512',
            'ram_gb': '16',
            'cpu': cls.price_cpu,
            'os': cls.price_os,
            'graphics': cls.price_graphics,
            'cpu_speed': '2.4',
            'total_sales': '30000',
        }

    def test_01_home_page_get_returns_200(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_02_price_page_get_returns_200(self):
        response = self.client.get(reverse('predict_price'))
        self.assertEqual(response.status_code, 200)

    def test_03_patterns_page_get_returns_200(self):
        response = self.client.get(reverse('patterns'))
        self.assertEqual(response.status_code, 200)

    def test_04_home_page_contains_title(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'LaptopPilot')

    def test_05_price_page_contains_title(self):
        response = self.client.get(reverse('predict_price'))
        self.assertContains(response, 'LaptopPilot Price Predictor')

    def test_06_patterns_page_contains_design_pattern_section(self):
        response = self.client.get(reverse('patterns'))
        self.assertContains(response, 'Design Patterns')

    def test_07_home_page_has_predict_form(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'id="predictForm"')

    def test_08_price_page_has_form(self):
        response = self.client.get(reverse('predict_price'))
        self.assertContains(response, 'id="priceForm"')

    def test_09_brand_prediction_post_with_valid_data(self):
        response = self.client.post(reverse('index'), self.brand_post)
        self.assertEqual(response.status_code, 200)
        self.assertIn('predicted_brand', response.context)

    def test_10_brand_prediction_post_sets_country(self):
        response = self.client.post(reverse('index'), self.brand_post)
        self.assertIn('predicted_country', response.context)

    def test_11_brand_prediction_post_sets_top_3_scores(self):
        response = self.client.post(reverse('index'), self.brand_post)
        self.assertIn('top3', response.context)

    def test_12_brand_prediction_post_preserves_form_data(self):
        response = self.client.post(reverse('index'), self.brand_post)
        self.assertEqual(response.context['form_data']['price'], '52000')

    def test_13_brand_prediction_post_invalid_numeric_value(self):
        payload = self.brand_post.copy()
        payload['price'] = 'invalid'
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_14_brand_prediction_post_missing_price_field(self):
        payload = self.brand_post.copy()
        payload.pop('price')
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_15_brand_prediction_post_missing_cpu_field(self):
        payload = self.brand_post.copy()
        payload.pop('cpu')
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_16_brand_prediction_post_missing_os_field(self):
        payload = self.brand_post.copy()
        payload.pop('os')
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_17_brand_prediction_post_missing_graphics_field(self):
        payload = self.brand_post.copy()
        payload.pop('graphics')
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_18_brand_prediction_post_negative_values_are_handled(self):
        payload = self.brand_post.copy()
        payload['ram_gb'] = '-4'
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)

    def test_19_brand_prediction_post_unrecognized_cpu_value(self):
        payload = self.brand_post.copy()
        payload['cpu'] = 'DefinitelyNotAValidCPU'
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_20_brand_prediction_post_unrecognized_os_value(self):
        payload = self.brand_post.copy()
        payload['os'] = 'FantasyOS'
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_21_brand_prediction_post_unrecognized_graphics_value(self):
        payload = self.brand_post.copy()
        payload['graphics'] = 'ImaginaryGPU'
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_22_brand_prediction_post_with_zero_price(self):
        payload = self.brand_post.copy()
        payload['price'] = '0'
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)

    def test_23_brand_prediction_post_with_blank_value(self):
        payload = self.brand_post.copy()
        payload['rating'] = ''
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_24_price_prediction_post_with_valid_data(self):
        response = self.client.post(reverse('predict_price'), self.price_post)
        self.assertEqual(response.status_code, 200)
        self.assertIn('predicted_price', response.context)

    def test_25_price_prediction_post_sets_brand_country(self):
        response = self.client.post(reverse('predict_price'), self.price_post)
        self.assertIn('predicted_country', response.context)

    def test_26_price_prediction_post_sets_map_location(self):
        response = self.client.post(reverse('predict_price'), self.price_post)
        self.assertIn('map_location', response.context)

    def test_27_price_prediction_post_preserves_selected_brand(self):
        response = self.client.post(reverse('predict_price'), self.price_post)
        self.assertEqual(response.context['form_data']['brand'], self.price_brand)

    def test_28_price_prediction_post_invalid_rating(self):
        payload = self.price_post.copy()
        payload['rating'] = 'invalid'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_29_price_prediction_post_missing_brand(self):
        payload = self.price_post.copy()
        payload.pop('brand')
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_30_price_prediction_post_missing_cpu(self):
        payload = self.price_post.copy()
        payload.pop('cpu')
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_31_price_prediction_post_missing_total_sales(self):
        payload = self.price_post.copy()
        payload.pop('total_sales')
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)

    def test_32_price_prediction_post_missing_cpu_speed(self):
        payload = self.price_post.copy()
        payload.pop('cpu_speed')
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)

    def test_33_price_prediction_post_negative_ram(self):
        payload = self.price_post.copy()
        payload['ram_gb'] = '-2'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)

    def test_34_price_prediction_post_unrecognized_brand(self):
        payload = self.price_post.copy()
        payload['brand'] = 'UnknownBrand'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('error', response.context)

    def test_35_price_prediction_post_unrecognized_cpu(self):
        payload = self.price_post.copy()
        payload['cpu'] = 'NotARealCPU'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_36_price_prediction_post_unrecognized_os(self):
        payload = self.price_post.copy()
        payload['os'] = 'NotAnOperatingSystem'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_37_price_prediction_post_unrecognized_graphics(self):
        payload = self.price_post.copy()
        payload['graphics'] = 'NoSuchGraphicsCard'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_38_price_prediction_post_with_blank_screen_size(self):
        payload = self.price_post.copy()
        payload['screen_size'] = ''
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_39_price_prediction_post_with_zero_storage(self):
        payload = self.price_post.copy()
        payload['storage_gb'] = '0'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)

    def test_40_price_prediction_post_with_large_values(self):
        payload = self.price_post.copy()
        payload['storage_gb'] = '4096'
        payload['ram_gb'] = '128'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)

    def test_40a_brand_prediction_rejects_unrealistic_values(self):
        payload = self.brand_post.copy()
        payload['price'] = '2000000'
        payload['ram_gb'] = '14000'
        payload['storage_gb'] = '20000'
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_40b_price_prediction_rejects_unrealistic_cpu_speed(self):
        payload = self.price_post.copy()
        payload['cpu_speed'] = '99.0'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_40c_price_prediction_rejects_unrealistic_price_and_storage(self):
        payload = self.price_post.copy()
        payload['total_sales'] = '100000000'
        payload['storage_gb'] = '12000'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_41_brand_helper_safe_encode_known_value(self):
        encoded = views._safe_encode(views.le_cpu, views.CPU_CHOICES[0])
        self.assertIsInstance(encoded, numbers.Integral)

    def test_42_brand_helper_safe_encode_unknown_value(self):
        encoded = views._safe_encode(views.le_cpu, 'ThisValueShouldNotExist')
        self.assertEqual(encoded, 0)

    def test_43_brand_helper_origin_known_brand(self):
        country, location = views._brand_origin('Dell')
        self.assertEqual(country, 'United States')
        self.assertIn('lat', location)

    def test_44_brand_helper_origin_unknown_brand(self):
        country, location = views._brand_origin('UnknownBrand')
        self.assertEqual(country, 'Global')
        self.assertIn('lat', location)

    def test_45_patterns_view_contains_creational_patterns(self):
        response = self.client.get(reverse('patterns'))
        self.assertContains(response, 'Creational')

    def test_46_patterns_view_contains_structural_patterns(self):
        response = self.client.get(reverse('patterns'))
        self.assertContains(response, 'Structural')

    def test_47_patterns_view_contains_behavioral_patterns(self):
        response = self.client.get(reverse('patterns'))
        self.assertContains(response, 'Behavioral')

    def test_48_patterns_view_has_ten_pattern_entries(self):
        response = self.client.get(reverse('patterns'))
        self.assertEqual(len(response.context['patterns']), 10)

    def test_49_project_model_values_are_loaded(self):
        self.assertTrue(hasattr(views, 'model'))
        self.assertTrue(hasattr(views, 'price_model'))

    def test_50_project_choice_lists_are_populated(self):
        self.assertTrue(views.CPU_CHOICES)
        self.assertTrue(views.OS_CHOICES)
        self.assertTrue(views.GRAPHICS_CHOICES)
        self.assertTrue(views.BRAND_CHOICES)

    def test_51_brand_feature_rules_are_defined_for_known_brand(self):
        rules = views.get_brand_feature_rules('Dell')
        self.assertIn('cpu_tokens', rules)
        self.assertIn('os_tokens', rules)
        self.assertIn('graphics_tokens', rules)

    def test_52_invalid_brand_feature_combo_is_rejected(self):
        payload = self.price_post.copy()
        payload['brand'] = 'Apple'
        payload['os'] = 'Windows 11'
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_53_brand_prediction_rejects_impossible_real_world_combo(self):
        payload = {
            'price': '52000',
            'rating': '4.5',
            'screen_size': '15.6',
            'storage_gb': '512',
            'ram_gb': '16',
            'cpu': 'Apple M1',
            'os': 'Windows 11',
            'graphics': 'NVIDIA GeForce RTX 4060',
        }
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertNotIn('predicted_brand', response.context)


class LaptopProjectRouteHealthTestCase(TestCase):
    def test_54_home_route_uses_index_template(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='template_user', email='template@example.com', password='StrongPass123', is_active=True)
        self.client.login(username='template_user', password='StrongPass123')
        response = self.client.get(reverse('index'))
        self.assertTrue(response.templates)

    def test_55_price_route_uses_price_template(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='price_template_user', email='price_template@example.com', password='StrongPass123', is_active=True)
        self.client.login(username='price_template_user', password='StrongPass123')
        response = self.client.get(reverse('predict_price'))
        self.assertTrue(response.templates)

    def test_56_patterns_route_uses_patterns_template(self):
        response = self.client.get(reverse('patterns'))
        self.assertTrue(response.templates)

    def test_56a_brand_predictor_requires_login(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_56b_price_predictor_requires_login(self):
        response = self.client.get(reverse('predict_price'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_57_signup_route_returns_200(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_58_forgot_password_route_returns_200(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)

    def test_59_login_page_has_signup_and_reset_links(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'signup')
        self.assertContains(response, 'forgot-password')

    def test_60_login_accepts_email_instead_of_username(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(username='demo_user', email='demo@example.com', password='StrongPass123', is_active=True)
        response = self.client.post(reverse('login'), {'username': 'demo@example.com', 'password': 'StrongPass123'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('_auth_user_id'), str(user.pk))

    def test_61_login_page_mentions_username_or_email(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Username or email')

    def test_61a_signup_rejects_username_matching_email(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'demo@example.com',
                'email': 'demo@example.com',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
        )
        self.assertContains(response, 'Username and email must be different')

    def test_62_login_page_has_password_field(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'id="password"')
        self.assertContains(response, 'password-toggle')
        self.assertContains(response, 'fa-eye')

    def test_63_signup_page_has_sign_in_link(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, 'Sign in')

    def test_64_verify_email_page_has_resend_link(self):
        response = self.client.get(reverse('verify_email', args=['dW5rZWFkeQ', 'badtoken']))
        self.assertContains(response, 'Resend verification email')

    def test_65_reset_password_rejects_reused_password(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        User = get_user_model()
        user = User.objects.create_user(username='reuse_user', email='reuse@example.com', password='OldPass123', is_active=True)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.post(
            reverse('reset_password', args=[uidb64, token]),
            {'password1': 'OldPass123', 'password2': 'OldPass123'}
        )

        self.assertContains(response, 'previously used password')


class LaptopFrontendBlackBoxTestCase(TestCase):
    """Black-box validation for the browser-facing inputs and UI flows."""

    def test_bb_01_brand_prediction_form_has_required_fields(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'id="price"')
        self.assertContains(response, 'id="rating"')
        self.assertContains(response, 'id="screen_size"')
        self.assertContains(response, 'id="storage_gb"')
        self.assertContains(response, 'id="ram_gb"')
        self.assertContains(response, 'id="cpu"')
        self.assertContains(response, 'id="os"')
        self.assertContains(response, 'id="graphics"')
        self.assertContains(response, 'required')

    def test_bb_02_price_prediction_form_has_required_fields(self):
        response = self.client.get(reverse('predict_price'))
        self.assertContains(response, 'id="brand"')
        self.assertContains(response, 'id="rating"')
        self.assertContains(response, 'id="screen_size"')
        self.assertContains(response, 'id="storage_gb"')
        self.assertContains(response, 'id="ram_gb"')
        self.assertContains(response, 'id="cpu_speed"')
        self.assertContains(response, 'id="total_sales"')
        self.assertContains(response, 'id="cpu"')
        self.assertContains(response, 'id="os"')
        self.assertContains(response, 'id="graphics"')

    def test_bb_03_invalid_brand_input_shows_user_error_message(self):
        payload = {
            'price': 'invalid',
            'rating': '4.5',
            'screen_size': '15.6',
            'storage_gb': '512',
            'ram_gb': '16',
            'cpu': 'Intel Core i5',
            'os': 'Windows 11',
            'graphics': 'NVIDIA GeForce RTX 4060',
        }
        response = self.client.post(reverse('index'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')

    def test_bb_04_invalid_price_input_shows_frontend_error(self):
        payload = {
            'brand': 'Dell',
            'rating': 'invalid',
            'screen_size': '14.0',
            'storage_gb': '512',
            'ram_gb': '16',
            'cpu': 'Intel Core i7',
            'os': 'Windows 11',
            'graphics': 'NVIDIA GeForce RTX 4060',
            'cpu_speed': '2.4',
            'total_sales': '30000',
        }
        response = self.client.post(reverse('predict_price'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')

    def test_bb_05_no_google_maps_key_falls_back_with_message(self):
        response = self.client.get(reverse('index'))
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if api_key:
            self.assertNotContains(response, 'Map preview is unavailable until a Google Maps key is configured.')
        else:
            self.assertContains(response, 'Map preview is unavailable until a Google Maps key is configured.')

    def test_bb_06_navigation_bar_exposes_primary_frontend_routes(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Price Predictor')
        self.assertContains(response, 'Design Patterns')
        self.assertContains(response, 'LaptopPilot')

    def test_bb_07_frontend_can_submit_new_defect(self):
        payload = {
            'defect_id': 'DEF-100',
            'severity': 'High',
            'priority': 'High',
            'module': 'Frontend Validation',
            'description': 'Submit button lacks disabled state during request',
            'root_cause': 'The UI does not visually indicate an in-flight request',
            'status': 'Open',
            'resolution': 'Add progress state on submit button',
        }
        response = self.client.post(reverse('patterns'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('DEF-100', str(response.context['defect_report']))


class LaptopFrontendWhiteBoxTestCase(TestCase):
    """White-box checks for the validation and normalization logic used by the frontend flow."""

    def test_wb_01_valid_ranges_pass_validation(self):
        validation = views._validate_realistic_laptop_inputs(
            price=65000,
            ram_gb=16,
            storage_gb=512,
            cpu_speed=2.4,
            total_sales=30000,
        )
        self.assertIsNone(validation)

    def test_wb_02_invalid_ranges_are_rejected(self):
        validation = views._validate_realistic_laptop_inputs(
            price=10000000,
            ram_gb=500,
            storage_gb=100000,
            cpu_speed=99.0,
            total_sales=400000000,
        )
        self.assertIsNotNone(validation)
        self.assertIn('unrealistic', validation.lower())

    def test_wb_03_token_matching_is_case_insensitive(self):
        self.assertTrue(views._matches_tokens('Intel Core i7', ['intel', 'core']))
        self.assertFalse(views._matches_tokens('NVIDIA RTX', ['amd', 'ryzen']))

    def test_wb_04_choice_resolution_norms_case_and_spaces(self):
        normalized = views._resolve_choice_value('windows 11', views.OS_CHOICES)
        self.assertIn(normalized, views.OS_CHOICES)

    def test_wb_05_compatible_brand_lookup_returns_expected_values(self):
        compatible = views.get_compatible_brands_for_features('Intel Core i7', 'Windows 11', 'NVIDIA GeForce RTX 4060')
        self.assertTrue(compatible)
        self.assertIn('Dell', compatible)

    def test_wb_06_unknown_brand_falls_to_global_origin(self):
        country, location = views._brand_origin('UnknownBrand')
        self.assertEqual(country, 'Global')
        self.assertIn('lat', location)
