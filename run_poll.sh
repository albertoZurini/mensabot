cd /opt/APPS/mensabot && \
if !git pull | grep -q 'Already up to date.'; then
  cd rust_telegram_bot;
  cargo build --release;
  cd ..
fi
./rust_telegram_bot/target/release/rust_telegram_bot
