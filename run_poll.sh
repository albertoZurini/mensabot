cd /opt/APPS/mensabot/rust && \
if ! git pull | grep -q 'Already up to date.'; then
  echo "Building"
  cargo build --release;
fi
./target/release/rust_telegram_bot
