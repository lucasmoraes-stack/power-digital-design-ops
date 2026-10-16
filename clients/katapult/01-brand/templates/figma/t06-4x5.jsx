const imgPhotoCard = "assets/d5a4012f-bb1f-4d59-8b1a-3957141fbdc9.png";
const imgVector12 = "assets/71d0536b-7912-48e9-a8e3-81025c8775d6.svg";
const imgKatapultLogoWhite = "assets/47ed55de-2b10-486d-8974-633667fbc4ff.svg";

export default function Template06TopBlockRoundedCard4X5() {
  return (
    <div className="bg-[#ed5370] relative size-full" data-node-id="547:1250" data-name="template-06-top-block-rounded-card-4x5">
      <div className="absolute h-[1262.636px] left-[-457px] mix-blend-soft-light top-[605px] w-[2429.41px]" data-node-id="547:1251">
        <div className="absolute inset-[-9.64%_-1.42%_-9.64%_0]">
          <img alt="" className="block max-w-none size-full" src={imgVector12} />
        </div>
      </div>
      <div className="absolute h-[480px] left-[30px] rounded-[48px] top-[662.62px] w-[1020px]" data-node-id="547:1252" data-name="photo-card">
        <div aria-hidden className="absolute inset-0 pointer-events-none rounded-[48px]">
          <img alt="" className="absolute max-w-none object-cover rounded-[48px] size-full" src={imgPhotoCard} />
          <div className="absolute bg-[rgba(0,0,0,0.25)] inset-0 rounded-[48px]" />
        </div>
      </div>
      <p className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-1/2 not-italic text-[15px] text-center text-white top-[1187.62px] w-[552px]" data-node-id="547:1253">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="-translate-x-1/2 absolute content-stretch flex flex-col gap-[48px] items-center left-1/2 top-[70px]" data-node-id="547:1254">
        <div className="content-stretch flex items-center relative shrink-0" data-node-id="547:1255">
          <div className="h-[31.616px] relative shrink-0 w-[142px]" data-node-id="547:1256" data-name="Katapult Logo (White)">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgKatapultLogoWhite} />
          </div>
        </div>
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[0] not-italic relative shrink-0 text-[112px] text-center text-white tracking-[-4.48px] w-[960px]" data-node-id="547:1262">
          <p className="leading-[0.9] mb-0">Time for the home</p>
          <p className="leading-[0.9]">upgrade you want.</p>
        </div>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] text-center w-[960px]" data-node-id="547:1263">
          No credit score needed. Just fair, straightforward terms.
        </p>
        <div className="bg-[#131540] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1264" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1264;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
    </div>
  );
}
