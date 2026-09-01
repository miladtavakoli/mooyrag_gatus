# Mooyrag Gatus

Uptime monitoring for Mooyrag sites. Gatus checks the endpoints; if one is down, `sms-webhook` sends SMS to the numbers in `SMS_TO`.

Dashboard: `http://127.0.0.1:9090`

## Setup

```bash
cp .env.example .env
# fill SMS_WEBHOOK_API_KEY, SMS_USERNAME, SMS_PASSWORD, SMS_FROM, SMS_TO, SMS_PANEL_URL
./deploy.sh
```

`SMS_TO` is comma-separated:

```
SMS_TO=09120000001,09120000002,09120000003
```

An alert SMS is sent after 3 failed checks, and again when the endpoint recovers.

## Test SMS

```bash
./test-alert.sh
./test-alert.sh "optional message"
```

## Logs

```bash
sudo docker compose logs -f gatus
sudo docker compose logs -f sms-webhook
```
